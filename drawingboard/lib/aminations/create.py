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
from drawingboard.lib.amination_templates import load as load_template
from drawingboard.lib.amination_templates import cli_to_str
from drawingboard.lib.ami_versions import load as load_ami

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def create_amination(name,description,ami_version,ami_version_base):

    name = unicode(name)
    description = unicode(description)

    ami_version = load_ami_version(ami_version_base,ami_version)
    ami_base = load_ami_base(ami_version['parent'])

    template = load_template_version(ami_base['template'],ami_version['template'])

    try:
        sqlite3_conn.execute("BEGIN TRANSACTION;")
        sqlite3_conn.execute("""INSERT INTO Aminations (
                `name`,
                `description`,
                `started`,
                `pid`,
                `template`,
                `amiversion`,
                `append_date`
            ) VALUES (:name,:description,:started,:pid,:template,:amiversion,:append_date)""",
            {
                "name" : name,
                "description" : description,
                "started" : False,
                "pid" : -1,
                "template" : template['id'],
                "amiversion" : ami_version['id'],
                "append_date" : True,
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
    except Exception as e:
        sqlite3_conn.execute("ROLLBACK;")
        raise e

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
            'value' : ami['name'] 
        })

    
    if not ami['regions']:
        raise RuntimeError("Could not determine regions to use! Should be stored in ami version")

    from_region='us-west-1'
    _regions = []
    for region in ami['regions']:
        if region['region'] != from_region:
            _regions.append(region['region'])


    amination_dir = '/etc/drawingboard/aminations/'+amination['cache_key']
    mkdir_p(amination_dir)

    aminator_command = 'aminate '+cli_to_str(template['cli'])+' '+template['provisioner']
    
    to_regions=";".join(_regions)

    _root = _dir = os.path.dirname(os.path.realpath(constants.__file__))+"/bin"
    #_dir = os.path.dirname(os.path.realpath(__file__))
    cli = [
        '/etc/drawingboard/bin/drawingboard_amination'
        '"'+amination_dir+'"',
        '"'+aminator_command+'"',
        '"'+from_region+'"',
        '"'+to_regions+'"'
    ]

    _process = subprocess.Popen(cli)
    
    sqlite3_conn.execute("UPDATE Aminations SET started = 1, pid =:pid WHERE id = :id",
        {
            "pid" : _process.pid,
            "id" : amination['id']
        }
    )
