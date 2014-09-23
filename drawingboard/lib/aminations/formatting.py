# coding: utf-8

from drawingboard.lib.tags import formatted_row as tag_formatted_row

def _base(row):
    r = {
        'id' : int(row['id']),
        'name' : row['name'],
        'description' : row['description'],
        'cache_key' : unicode(row['cache_key']),
        'started' : bool(row['started']),
        'template' : row['template'],
        'amiversion' : row['amiversion'],
        'append_date' : bool(row['append_date']),
        'created' : row['created'],
    }

    return r

def formatted_row(row):
    base = _base(row)

    if base['append_date']:
        base['name']+="-"+base['created']

    return base
    