# coding: utf-8

import json

from drawingboard.lib.tags import formatted_row as tag_formatted_row
from drawingboard.lib.aws_regions import formatted_row as region_formatted_row

def _base(row,tags,regions,versions):
    r = {
        'id' : int(row['id']),
        'version' : unicode(row['version']),
        'parent' : int(row['parent']),
        'template' : int(row['template']),
        'name' : row['name'],
        'description' : row['description'],
        'append_date' : bool(row['append_date']),
        'append_version' : bool(row['append_version']),
        'created' : row['created'],
        'tags' : [],
        'regions' : [],
        'base_region' : "",
        'versions' : versions
    }

    base_region = None
    for region in regions:
        if region['base']:
            r['base_region'] = region['region']

    if not r['base_region'] and regions:
        raise RuntimeError("Unable to load base region for ami version %s" % r['id'])

    for tag in tags:
        r['tags'].append(
            tag_formatted_row(tag)
        )

    for region in regions:
        if not region['base']:
            r['regions'].append(
                region_formatted_row(region)
            )

    return r

def formatted_row(row,tags,regions,versions):
    if row['parent'] == 0:
        return formatted_base_row(row,tags,regions,versions)
    else:
        return formatted_version_row(row,tags,regions,versions)

def formatted_version_row(row,tags,regions,versions):
    base = _base(row,tags,regions,versions)

    if base['append_version']:
        base['name']+="-v"+base['version']

    if base['append_date']:
        base['name']+="-"+base['created']

    del base['versions']
    
    return base

def formatted_base_row(row,tags,regions,versions):
    return _base(row,tags,regions,versions)
    