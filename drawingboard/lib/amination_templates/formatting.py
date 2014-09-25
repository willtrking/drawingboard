# coding: utf-8

import json
import re

from drawingboard.lib.tags import formatted_row as tag_formatted_row

escape_reg = re.compile('([^0-9a-zA-Z]+)')

def _escape(str):
    """
        You're probably thinking 'uh, pipes.quote() maybe?'
        This would work IF we were simply passing these CLI vars to a single bash script
        But we're not. We're proxying them through another bash script first

        These ended up being the most reliable way to handle all possibilities.
        Remember also that bash doesn't care if you escape all non-alphanumeric characters
    """
    _str = escape_reg.split(str)
    _final = ''

    for _s in _str:
        if _s != '':
            if _s.isalnum():
                _final += _s
            else:
                _final += '\\'+_s

    return _final

def cli_to_str(args,escape=False):
    _str = ""
    for arg in args:
        if arg['name']:
            _str+=" "+arg['name']

        if arg['value']:
            if escape:
                _str+=" "+_escape(arg['value'])
            else:
                _str+=" "+arg['value']
    
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
    