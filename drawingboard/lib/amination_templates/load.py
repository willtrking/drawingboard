# coding: utf-8

from .formatting import formatted_row
from drawingboard.db import sqlite3_conn

def all_tags():
    with sqlite3_conn:
        tags = sqlite3_conn.execute("""SELECT Tags.*, AminationTemplatesTags.template FROM AminationTemplatesTags 
            INNER JOIN Tags ON AminationTemplatesTags.tag = Tags.id"""
        ).fetchall()

    return tags

def tags_for_template(template):
    with sqlite3_conn:
        tags = sqlite3_conn.execute("""SELECT Tags.* FROM AminationTemplatesTags 
            INNER JOIN Tags ON AminationTemplatesTags.tag = Tags.id WHERE AminationTemplatesTags.template = :id""",
            {"id":template}
        ).fetchall()

    return tags

def load(template):
    with sqlite3_conn:
        base = sqlite3_conn.execute("SELECT * FROM AminationTemplates WHERE id = :template LIMIT 1;",
            {"template":template}
        ).fetchone()

    tags = tags_for_template(base['id'])

    return formatted_row(base,tags)

def load_base(base):
    with sqlite3_conn:
        base = sqlite3_conn.execute("SELECT * FROM AminationTemplates WHERE parent = 0 AND id = :id LIMIT 1;",{"id":base}).fetchone()

    tags = tags_for_template(base['id'])

    return formatted_row(base,tags)

def load_version(base,version):
    with sqlite3_conn:
        base = sqlite3_conn.execute("SELECT * FROM AminationTemplates WHERE parent = :parent AND id = :version LIMIT 1;",
            {"parent":base,"version":version}
        ).fetchone()

    tags = tags_for_template(base['id'])

    return formatted_row(base,tags)

def all_bases():
    with sqlite3_conn:
        bases = sqlite3_conn.execute("SELECT * FROM AminationTemplates WHERE parent = 0 ORDER BY id,created ASC").fetchall()

    tags = all_tags()
    _tags = {}
    for tag in tags:
        _id = int(tag['template'])
        if _id not in _tags:
            _tags[_id] = []   
        
        _tags[_id].append(tag)

    _bases = []
    for base in bases:

        _t = []
        try:
            _t = _tags[int(base['id'])]
        except:
            pass

        _bases.append(formatted_row(
            base,
            _t
        ))

    return _bases


def all_versions():
    with sqlite3_conn:
        bases = sqlite3_conn.execute("SELECT * FROM AminationTemplates WHERE parent != 0 ORDER BY id,created ASC").fetchall()

    tags = all_tags()
    _tags = {}
    for tag in tags:
        _id = int(tag['template'])
        if _id not in _tags:
            _tags[_id] = []   
        
        _tags[_id].append(tag)

    _bases = []
    for base in bases:

        _t = []
        try:
            _t = _tags[int(base['id'])]
        except:
            pass

        _bases.append(formatted_row(
            base,
            _t
        ))

    return _bases

def versions_for_base(parent):
    with sqlite3_conn:
        versions = sqlite3_conn.execute(
            "SELECT * FROM AminationTemplates WHERE parent = :id ORDER BY version,created ASC",
            {"id":parent}
        ).fetchall()

    tags = all_tags()
    _tags = {}
    for tag in tags:
        _id = int(tag['template'])
        if _id not in _tags:
            _tags[_id] = []   
        
        _tags[_id].append(tag)

    _versions = []
    for version in versions:
        _t = []
        try:
            _t = _tags[int(base['id'])]
        except:
            pass

        _versions.append(formatted_row(
            version,
            _t
        ))

    return _versions