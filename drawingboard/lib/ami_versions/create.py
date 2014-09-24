# coding: utf-8

import json
from .load import regions_for_version, tags_for_version, load_base
from drawingboard.db import sqlite3_conn
from drawingboard.lib.tags import add_tags, retrieve_tags
from drawingboard.lib.aws_regions import retrieve_regions
from drawingboard.lib.amination_templates import load_version as load_template_version
from drawingboard.lib.amination_templates import load_base as load_base_template

def _increment_version(version):
    return int(version) + 1

def create_base_version(template,
        name,append_date,append_version,
        tags,description):

    
    template = load_base_template(template)

    if not template:
        raise RuntimeError("Unable to find base template with id %s" % template)

    version = 0
    parent = 0
    name = unicode(name)
    description = unicode(description)
    
    try:
        sqlite3_conn.execute("BEGIN TRANSACTION;")
        sqlite3_conn.execute("""INSERT INTO AMIVersions (
                `version`,
                `parent`,
                `template`,
                `name`,
                `description`,
                `append_date`,
                `append_version`
            ) VALUES (:version,:parent,:template,:name,:description,:append_date,:append_version)""",
            {
                "version" : 0,
                "parent" : 0,
                "template" : template['id'],
                "name" : name,
                "description" : description,
                "append_date" : int(append_date),
                "append_version" : int(append_version)
            }
        )
        _last_id = sqlite3_conn.execute("SELECT last_insert_rowid()").fetchone()

        add_tags(tags,conn=sqlite3_conn)
        _tags = retrieve_tags(tags,require_all=True)
        _insert_tags = []
        for _tag in _tags:
            _insert_tags.append(
                (_tag['id'],_last_id[0],)
            )

        sqlite3_conn.executemany("INSERT INTO AMIVersionsTags(`tag`,`amiversion`) VALUES (?,?)",_insert_tags)

        sqlite3_conn.execute("COMMIT TRANSACTION;")
    except Exception as e:
        sqlite3_conn.execute("ROLLBACK TRANSACTION;")
        raise e

def create_version_version(parent,template,base_region,regions):
    
    parent_version = load_base(parent)

    template = load_template_version(parent_version['template'],template)

    if not template:
        raise RuntimeError("Unable to find base template with id %s" % template)

    tags = tags_for_version(parent)

    regions.append(base_region)
    regions = retrieve_regions(regions,require_all=True)

    try:
        sqlite3_conn.execute('BEGIN EXCLUSIVE TRANSACTION;')

        versions = sqlite3_conn.execute("SELECT * FROM AMIVersions WHERE parent = :id ORDER BY id DESC LIMIT 1;",{"id":parent}).fetchone()

        if not versions:
            version = 1
        else:
            version = _increment_version(versions['version'])

        parent = parent_version['id']
        name = parent_version['name']
        description = parent_version['description']

        append_date = parent_version['append_date']
        append_version = parent_version['append_version']

        sqlite3_conn.execute("""INSERT INTO AMIVersions (
                `version`,
                `parent`,
                `template`,
                `name`,
                `description`,
                `append_date`,
                `append_version`
            ) VALUES (:version,:parent,:template,:name,:description,:append_date,:append_version)""",
            {
                "version" : version,
                "parent" : parent,
                "template" : template['id'],
                "name" : name,
                "description" : description,
                "append_date" : int(append_date),
                "append_version" : int(append_version)
            }
        )
        _last_id = sqlite3_conn.execute("SELECT last_insert_rowid()").fetchone()

        _insert_tags = []
        for _tag in tags:
            _insert_tags.append(
                (_tag['id'],_last_id[0],)
            )

        sqlite3_conn.executemany("INSERT INTO AMIVersionsTags(`tag`,`amiversion`) VALUES (?,?)",_insert_tags)

        _insert_regions = []
        for _region in regions:
            base = 0
            if _region['region'] == base_region:
                base = 1
            
            _insert_regions.append(
                (_region['id'],_last_id[0],base,)
            )

        sqlite3_conn.executemany("INSERT INTO AMIVersionsRegions(`region`,`amiversion`,`base`) VALUES (?,?,?)",_insert_regions)


        sqlite3_conn.execute('COMMIT TRANSACTION;')
    except Exception as e:
        sqlite3_conn.execute('ROLLBACK TRANSACTION;')
        raise e


        

