# coding: utf-8

from .formatting import formatted_row
from drawingboard.db import sqlite3_conn    

def retrieve_tags(tags,require_all=True):
    _tags = []
    for tag in tags:
        _tag = sqlite3_conn.execute("SELECT * FROM Tags WHERE tag = :tag LIMIT 1;",{"tag":tag}).fetchone()
        if not _tag and require_all:
            raise RuntimeError("Missing tag %s" % tag)
                
        if _tag:
            _tags.append(_tag)

    return _tags

def all_tags():
    tags = sqlite3_conn.execute("SELECT * FROM Tags").fetchall()

    _tags = []
    for tag in tags:
        _tags.append(formatted_row(tag))

    return _tags

