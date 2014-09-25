# coding: utf-8

from .formatting import formatted_row
from drawingboard.db import sqlite3_conn
from drawingboard.lib.ami_versions import load as load_ami

def _load_file(file):
    try:
        with open(file,'r') as f:
            return f.read()
    except:
        return None
    return None

def all_base_aminations():
    with sqlite3_conn:
        bases = sqlite3_conn.execute("SELECT * FROM Aminations WHERE parent = 0 ORDER BY id,created ASC").fetchall()

    _bases = []
    for base in bases:

        _bases.append(_load(base))

    return _bases

def aminations_for_base(base):
    with sqlite3_conn:
        bases = sqlite3_conn.execute("SELECT * FROM Aminations WHERE parent = :base ORDER BY id,created ASC",
            {"base":base}
        ).fetchall()

    _bases = []
    for base in bases:

        _bases.append(_load(base))

    return _bases

def load(amination):
    with sqlite3_conn:
        base = sqlite3_conn.execute("SELECT * FROM Aminations WHERE id = :amination LIMIT 1;",
            {"amination":amination}
        ).fetchone()
    return _load(base)

def load_base(amination):
    with sqlite3_conn:
        base = sqlite3_conn.execute("SELECT * FROM Aminations WHERE id = :amination AND parent = 0 LIMIT 1;",
            {"amination":amination}
        ).fetchone()
    return _load(base)

def load_version(base,version):
    with sqlite3_conn:
        base = sqlite3_conn.execute("SELECT * FROM Aminations WHERE id = :version AND parent = :base LIMIT 1;",
            {"base":base,"version":version}
        ).fetchone()
    return _load(base)

def _load(base):

    exit_code = None
    ami_id = None
    stdout = None
    stderr = None
    aminator_exit_code = None
    region_exit_codes = {}
    region_ami_ids = {}

    if base['started']:
        ami = load_ami(base['amiversion'])

        cache_path = '/etc/drawingboard/aminations/%s' % base['cache_key']

        #Vars
        exit_code = _load_file('%s/exit_code' % cache_path)
        ami_id = _load_file('%s/ami_id' % cache_path)
        stdout = _load_file('%s/stdout' % cache_path)
        stderr = _load_file('%s/stderr' % cache_path)
        aminator_exit_code = _load_file('%s/aminator_exit_code' % cache_path)

        for region in ami['regions']:
            if region['region'] == ami['base_region']:
                region_exit_codes[region['region']] = aminator_exit_code
                region_ami_ids[region['region']] = ami_id
            else:
                region_exit_codes[region['region']] = _load_file('%s/region_ami_id_exit_code_%s' % (
                    cache_path,
                    region['region']
                ))

                region_ami_ids[region['region']] = _load_file('%s/region_ami_id_exit_code_%s' % (
                    cache_path,
                    region['region']
                ))

    return formatted_row(
        row=base,
        exit_code=exit_code,
        ami_id=ami_id,
        stdout=stdout,
        stderr=stderr,
        aminator_exit_code=aminator_exit_code,
        region_exit_codes=region_exit_codes,
        region_ami_ids=region_ami_ids
    )