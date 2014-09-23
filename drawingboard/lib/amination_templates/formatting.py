# coding: utf-8

import json

from drawingboard.lib.tags import formatted_row as tag_formatted_row

def cli_to_str(args):
    _str = ""
    for arg in args:
        if arg['name']:
            _str+=" "+arg['name']

        if arg['value']:
            if arg['name']:
                if arg['value'][0] != "'":
                    _str+=" '"+arg['value']+"'"
                else:
                    _str+=" "+arg['value']

            else:
                _str+=arg['value']
    
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
    