# coding: utf-8

import os, errno
import subprocess
import shlex
from .load import load as load_amination
from drawingboard import constants
from drawingboard.db import sqlite3_conn
from drawingboard.lib.ami_versions import load_version as load_ami_version
from drawingboard.lib.ami_versions import load_base as load_ami_base 
from drawingboard.lib.amination_templates import load_version as load_template_version
from drawingboard.lib.amination_templates import load_base as load_template_base
from drawingboard.lib.amination_templates import load as load_template
from drawingboard.lib.amination_templates import cli_to_str
from drawingboard.lib.ami_versions import load as load_ami

from drawingboard.lib.aminations import load_base as load_base_amination

def _increment_version(version):
    return int(version) + 1

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def create_base_amination(name,description,ami_version_base):

    name = unicode(name)
    description = unicode(description)

    ami_base = load_ami_base(ami_version_base)

    template = load_template_base(ami_base['template'])

    try:
        sqlite3_conn.execute("BEGIN TRANSACTION;")
        sqlite3_conn.execute("""INSERT INTO Aminations (
                `version`,
                `parent`,
                `name`,
                `description`,
                `started`,
                `template`,
                `amiversion`,
                `append_date`,
                `append_version`
            ) VALUES (:version,:parent,:name,:description,:started,:template,:amiversion,:append_date,:append_version)""",
            {
                "version" : 0,
                "parent" : 0,
                "name" : name,
                "description" : description,
                "started" : False,
                "template" : template['id'],
                "amiversion" : ami_base['id'],
                "append_date" : True,
                "append_version" : True
            }
        )

        _last_id = sqlite3_conn.execute("SELECT last_insert_rowid()").fetchone()
        cache_key = "amination_"+str(_last_id[0])

        sqlite3_conn.execute("UPDATE Aminations SET cache_key = :cache_key WHERE id = :id",
            {
                "cache_key" : cache_key,
                "id" : _last_id[0]
            }
        )

        sqlite3_conn.execute("COMMIT;")
        return _last_id[0]
    except Exception as e:
        sqlite3_conn.execute("ROLLBACK;")
        raise e

    return None
    

def create_amination_version(amination_base,ami_version,start=False):
    parent_amination = load_base_amination(amination_base)

    ami_version = load_ami_version(parent_amination['amiversion'],ami_version)
    template = load_template_version(parent_amination['template'],ami_version['template'])
    try:
        sqlite3_conn.execute('BEGIN EXCLUSIVE TRANSACTION;')
        parent = parent_amination['id']

        versions = sqlite3_conn.execute("SELECT * FROM Aminations WHERE parent = :id ORDER BY id DESC LIMIT 1;",{"id":parent}).fetchone()

        if not versions:
            version = 1
        else:
            version = _increment_version(versions['version'])

        name = parent_amination['name']
        description = parent_amination['description']
        append_date = parent_amination['append_date']
        append_version = parent_amination['append_version']
        

        sqlite3_conn.execute("""INSERT INTO Aminations (
                `version`,
                `parent`,
                `name`,
                `description`,
                `started`,
                `template`,
                `amiversion`,
                `append_date`,
                `append_version`
            ) VALUES (:version,:parent,:name,:description,:started,:template,:amiversion,:append_date,:append_version)""",
            {
                "version" : version,
                "parent" : parent,
                "name" : name,
                "description" : description,
                "started" : False,
                "template" : template['id'],
                "amiversion" : ami_version['id'],
                "append_date" : append_date,
                "append_version" : append_version
            }
        )

        _last_id = sqlite3_conn.execute("SELECT last_insert_rowid()").fetchone()
        cache_key = parent_amination['cache_key']+"_"+str(_last_id[0])

        sqlite3_conn.execute("UPDATE Aminations SET cache_key = :cache_key WHERE id = :id",
            {
                "cache_key" : cache_key,
                "id" : _last_id[0]
            }
        )
        sqlite3_conn.execute("COMMIT;")
        if start:
            return start_amination(_last_id[0])
        else:
            return _last_id[0]
    except Exception as e:
        import traceback
        traceback.print_exc()
        sqlite3_conn.execute("ROLLBACK;")
        raise e

    return None


def start_amination(amination):
    amination = load_amination(amination)

    template = load_template(amination['template'])
    ami = load_ami(amination['amiversion'])

    _cli = template['cli']
    _has_name = False
    for arg in _cli:
        if arg['name'].strip() == '-n':
            _has_name = True

    if not _cli:
        raise RuntimeError("Could not determine CLI args to use! Should be stored in amination template")

    if not _has_name:
        _cli.append({
            'name' : '-n',
            'value' : '['+ami['name']+']-'+amination['created']
        })

    
    if not ami['regions']:
        raise RuntimeError("Could not determine regions to use! Should be stored in ami version")

    if not ami['base_region']:
        raise RuntimeError("Could not determine base region to use! Should be stored in ami version")

    from_region=ami['base_region']
    _regions = []
    for region in ami['regions']:
        if region['region'] != from_region:
            _regions.append(region['region'])


    amination_dir = '/etc/drawingboard/aminations/'+amination['cache_key']
    cli_status_file = "%s/exit_code"
    mkdir_p(amination_dir)

    aminator_command = 'aminate '+cli_to_str(template['cli'])+' '+template['provisioner']
    
    to_regions=";".join(_regions)
    command = "/etc/drawingboard/bin/drawingboard_amination '%s' '%s' '%s' '%s' -- ; echo $? > %s" % (
        amination_dir,
        aminator_command,
        from_region,
        to_regions,
        cli_status_file
    )
    cli = [
        "/bin/bash",
        "-c",
        command
    ]
    _process = subprocess.Popen(
        cli,
        stdin=None,
        stdout=None,
        stderr=None,
        close_fds=True
    )
    
    sqlite3_conn.execute("UPDATE Aminations SET started = 1, pid =:pid WHERE id = :id",
        {
            "pid" : _process.pid,
            "id" : amination['id']
        }
    )

