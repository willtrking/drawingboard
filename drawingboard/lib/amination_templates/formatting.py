# coding: utf-8

import json
import re

from drawingboard.lib.tags import formatted_row as tag_formatted_row

escape_reg = re.compile('([^0-9a-zA-Z]+)')

def escape(str):
    _str = escape_reg.split(str)
    print _str
    _final = ''
    for _s in _str:
        if _s != '':
            if _s.isalnum():
                _final += _s
            else:
                _final += '\\\\'+_s

    return _final

def cli_to_str(args):
    _str = ""
    for arg in args:
        if arg['name']:
            _str+=" "+arg['name']

        if arg['value']:
            
            _str+=" "+escape(arg['value'])
    
    return _str.strip()

def _format_cli_args(args):
    args = json.loads(args)
    return args

def _base(row,tags):
    r = {
        'id' : int(row['id']),
        'version' : unicode(row['version']),
        'parent' : int(row['parent']),
        'name' : row['name'],
        'description' : row['description'],
        'provisioner' : row['provisioner'],
        'append_date' : bool(row['append_date']),
        'append_version' : bool(row['append_version']),
        'cli' : _format_cli_args(row['cli']),
        'created' : row['created'],
        'tags' : []
    }

    for tag in tags:
        r['tags'].append(
            tag_formatted_row(tag)
        )

    return r

def formatted_row(row,tags):
    if row['parent'] == 0:
        return formatted_base_row(row,tags)
    else:
        return formatted_version_row(row,tags)

def formatted_version_row(row,tags):
    base = _base(row,tags)

    if base['append_version']:
        base['name']+="-v"+base['version']

    if base['append_date']:
        base['name']+="-"+base['created']

    return base

def formatted_base_row(row,tags):
    return _base(row,tags)
    