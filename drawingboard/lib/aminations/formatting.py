# coding: utf-8

from drawingboard.lib.tags import formatted_row as tag_formatted_row

def exit_code_status(code):
    try:
        code = int(code)
    except:
        return "PyError: Unable to calculate exit code!"

    if code == 0:
        return "Success!"
    elif code == 127:
        return "ERROR: Command not found! (127)"
    
    return "ERROR: Exit code %s" % code


def _base(row,exit_code,
        ami_id,stdout,stderr,
        aminator_exit_code,
        aminator_command,
        region_exit_codes,
        region_ami_ids):
    r = {
        'id' : int(row['id']),
        'version' : unicode(row['version']),
        'parent' : int(row['parent']),
        'id' : int(row['id']),
        'name' : row['name'],
        'description' : row['description'],
        'cache_key' : unicode(row['cache_key']),
        'started' : bool(row['started']),
        'template' : row['template'],
        'amiversion' : row['amiversion'],
        'append_date' : bool(row['append_date']),
        'append_version' : bool(row['append_version']),
        'created' : row['created'],
        'exit_code' : exit_code.strip() if exit_code is not None else '',
        'ami_id' : ami_id.strip() if ami_id is not None else '',
        'aminator_exit_code' : aminator_exit_code.strip() if aminator_exit_code is not None else '',
        'stdout' : stdout if stdout is not None else '',
        'stderr' : stderr if stderr is not None else '',
        'region_exit_codes' : {},
        'region_ami_ids' : {}
    }

    for _region,code in region_exit_codes.iteritems():
        r['region_exit_codes'][_region] = code.strip() if code is not None else ''

    for _region,ami in region_ami_ids.iteritems():
        r['region_ami_ids'][_region] = ami.strip() if ami is not None else ''

    r['status'] = ""
    if not bool(r['started']):
        r['status'] = "Not Started"
    else:
        if not r['exit_code']:
            r['status'] = "Running"
        else:
            r['status'] = exit_code_status(r['exit_code'])

    return r


def formatted_row(row,exit_code,
        ami_id,stdout,stderr,
        aminator_exit_code,
        aminator_command,
        region_exit_codes,
        region_ami_ids):
    if row['parent'] == 0:
        return formatted_base_row(row,exit_code,
            ami_id,stdout,stderr,
            aminator_exit_code,
            region_exit_codes,
            region_ami_ids
        )
    else:
        return formatted_version_row(row,exit_code,
            ami_id,stdout,stderr,
            aminator_exit_code,
            region_exit_codes,
            region_ami_ids
        )

def formatted_version_row(row,exit_code,
        ami_id,stdout,stderr,
        aminator_exit_code,
        aminator_command,
        region_exit_codes,
        region_ami_ids):
    base = _base(row,exit_code,
        ami_id,stdout,stderr,
        aminator_exit_code,
        region_exit_codes,
        region_ami_ids
    )

    if base['append_version']:
        base['name']+="-v"+base['version']

    if base['append_date']:
        base['name']+="-"+base['created']

    return base

def formatted_base_row(row,exit_code,
        ami_id,stdout,stderr,
        aminator_exit_code,
        aminator_command,
        region_exit_codes,
        region_ami_ids):
    return _base(row,exit_code,
        ami_id,stdout,stderr,
        aminator_exit_code,
        region_exit_codes,
        region_ami_ids)
    