# coding: utf-8

import json
from .load import tags_for_template, load_base
from drawingboard.db import sqlite3_conn
from drawingboard.lib.tags import add_tags, retrieve_tags

def _increment_version(version):
    return int(version) + 1

def create_base_template(name,
        append_date,append_version,
        tags,description,
        provisioner,cli_args):


    version = 0
    parent = 0
    name = unicode(name)
    description = unicode(description)
    provisioner = unicode(provisioner)

    _args = []
    for arg in cli_args:
        _args.append({
            'name':unicode(arg['name']),
            'value':unicode(arg['value']),
        })
    _args = json.dumps(_args)

    
    try:
        sqlite3_conn.execute("BEGIN TRANSACTION;")
        sqlite3_conn.execute("""INSERT INTO AminationTemplates (
                `version`,
                `parent`,
                `name`,
                `description`,
                `provisioner`,
                `cli`,
                `append_date`,
                `append_version`
            ) VALUES (:version,:parent,:name,:description,:provisioner,:cli,:append_date,:append_version)""",
            {
                "version" : 0,
                "parent" : 0,
                "name" : name,
                "description" : description,
                "provisioner" : provisioner,
                "cli" : _args,
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

        sqlite3_conn.executemany("INSERT INTO AminationTemplatesTags(`tag`,`template`) VALUES (?,?)",_insert_tags)

        sqlite3_conn.execute("COMMIT TRANSACTION;")
    except Exception as e:
        sqlite3_conn.execute("ROLLBACK TRANSACTION;")
        raise e

    


def create_template_version(parent,provisioner=None,cli_args=None):

    parent_template = load_base(parent)
    tags = tags_for_template(parent)

    try:
        sqlite3_conn.execute('BEGIN EXCLUSIVE TRANSACTION;')

        versions = sqlite3_conn.execute("SELECT * FROM AminationTemplates WHERE parent = :id ORDER BY id DESC LIMIT 1;",{"id":parent}).fetchone()

        if not versions:
            version = 1
        else:
            version = _increment_version(versions['version'])

        parent = parent_template['id']
        name = parent_template['name']
        description = parent_template['description']
        if provisioner is None:
            provisioner = parent_template['provisioner']
        else:
            provisioner = unicode(provisioner)

        if cli_args is None:
            cli_args = parent_template['cli']
        else:
            _args = []
            for arg in cli_args:
                _args.append({
                    'name':unicode(arg['name']),
                    'value':unicode(arg['value']),
                })
            cli_args = json.dumps(_args)

        append_date = parent_template['append_date']
        append_version = parent_template['append_version']

        sqlite3_conn.execute("""INSERT INTO AminationTemplates (
                `version`,
                `parent`,
                `name`,
                `description`,
                `provisioner`,
                `cli`,
                `append_date`,
                `append_version`
            ) VALUES (:version,:parent,:name,:description,:provisioner,:cli,:append_date,:append_version)""",
            {
                "version" : version,
                "parent" : parent,
                "name" : name,
                "description" : description,
                "provisioner" : provisioner,
                "cli" : cli_args,
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

        sqlite3_conn.executemany("INSERT INTO AminationTemplatesTags(`tag`,`template`) VALUES (?,?)",_insert_tags)

        sqlite3_conn.execute('COMMIT TRANSACTION;')
    except Exception as e:
        sqlite3_conn.execute('ROLLBACK TRANSACTION;')
        raise e


        

