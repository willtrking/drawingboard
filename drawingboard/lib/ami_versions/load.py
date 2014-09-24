# coding: utf-8

from .formatting import formatted_row
from drawingboard.db import sqlite3_conn

def all_tags():
    with sqlite3_conn:
        tags = sqlite3_conn.execute("""SELECT Tags.*, AMIVersionsTags.amiversion FROM AMIVersionsTags 
            INNER JOIN Tags ON AMIVersionsTags.tag = Tags.id"""
        ).fetchall()

    return tags

def tags_for_version(version):
    with sqlite3_conn:
        tags = sqlite3_conn.execute("""SELECT Tags.* FROM AMIVersionsTags 
            INNER JOIN Tags ON AMIVersionsTags.tag = Tags.id WHERE AMIVersionsTags.amiversion = :id""",
            {"id":version}
        ).fetchall()

    return tags

def all_regions():
    with sqlite3_conn:
        regions = sqlite3_conn.execute("""SELECT AWSRegions.*, AMIVersionsRegions.amiversion,AMIVersionsRegions.base AS base FROM AMIVersionsRegions 
            INNER JOIN AWSRegions ON AMIVersionsRegions.region = AWSRegions.id"""
        ).fetchall()

    return regions

def regions_for_version(version):
    with sqlite3_conn:
        regions = sqlite3_conn.execute("""SELECT AWSRegions.*,AMIVersionsRegions.base AS base FROM AMIVersionsRegions 
            INNER JOIN AWSRegions ON AMIVersionsRegions.region = AWSRegions.id WHERE AMIVersionsRegions.amiversion = :id""",
            {"id":version}
        ).fetchall()

    return regions

def load(base):
    with sqlite3_conn:
        base = sqlite3_conn.execute("SELECT * FROM AMIVersions WHERE id = :id LIMIT 1;",{"id":base}).fetchone()

    tags = tags_for_version(base['id'])
    regions = regions_for_version(base['id'])
    versions = versions_for_base(base['id'])

    return formatted_row(base,tags,regions,versions)

def load_base(base):
    with sqlite3_conn:
        base = sqlite3_conn.execute("SELECT * FROM AMIVersions WHERE parent = 0 AND id = :id LIMIT 1;",{"id":base}).fetchone()

    tags = tags_for_version(base['id'])
    regions = regions_for_version(base['id'])
    versions = versions_for_base(base['id'])

    return formatted_row(base,tags,regions,versions)

def load_version(base,version):
    with sqlite3_conn:
        base = sqlite3_conn.execute("SELECT * FROM AMIVersions WHERE parent = :base AND id = :version LIMIT 1;",
            {"base":base,"version":version}
        ).fetchone()

    tags = tags_for_version(base['id'])
    regions = regions_for_version(base['id'])

    return formatted_row(base,tags,regions,[])

def all_bases():
    with sqlite3_conn:
        bases = sqlite3_conn.execute("SELECT * FROM AMIVersions WHERE parent = 0 ORDER BY id,created ASC").fetchall()

    tags = all_tags()
    _tags = {}
    for tag in tags:
        _id = int(tag['amiversion'])
        if _id not in _tags:
            _tags[_id] = []   
        
        _tags[_id].append(tag)


    regions = all_regions()
    _regions = {}
    for region in regions:

        _id = int(region['amiversion'])
        if _id not in _regions:
            _regions[_id] = []   
        
        _regions[_id].append(region)

    _all_versions = all_versions()
    _versions = {}
    for _v in _all_versions:
        _id = int(_v['parent'])
        if _id not in _versions:
            _versions[_id] = []
        
        _versions[_id].append(_v)


    _bases = []
    for base in bases:

        _t = []
        try:
            _t = _tags[int(base['id'])]
        except:
            pass

        _r = []
        try:
            _r = _regions[int(base['id'])]
        except:
            pass

        _v = []
        try:
            _v = _versions[int(base['id'])]
        except:
            pass

        _bases.append(formatted_row(
            base,
            _t,
            _r,
            _v
        ))

    return _bases


def all_versions():
    with sqlite3_conn:
        versions = sqlite3_conn.execute(
            "SELECT * FROM AMIVersions ORDER BY created ASC"
        ).fetchall()

    tags = all_tags()
    _tags = {}
    for tag in tags:
        _id = int(tag['amiversion'])
        if _id not in _tags:
            _tags[_id] = []   
        
        _tags[_id].append(tag)


    regions = all_regions()
    _regions = {}
    for region in regions:
        
        _id = int(region['amiversion'])
        if _id not in _regions:
            _regions[_id] = []   
        
        _regions[_id].append(region)

    _versions = []
    for version in versions:
        _t = []
        try:
            _t = _tags[int(version['id'])]
        except:
            pass

        _r = []
        try:
            _r = _regions[int(version['id'])]
        except:
            pass

        _versions.append(formatted_row(
            version,
            _t,
            _r,
            -1
        ))

    return _versions


def versions_for_base(parent):
    with sqlite3_conn:
        versions = sqlite3_conn.execute(
            "SELECT * FROM AMIVersions WHERE parent = :id ORDER BY version,created ASC",
            {"id":parent}
        ).fetchall()

    tags = all_tags()
    _tags = {}
    for tag in tags:
        _id = int(tag['amiversion'])
        if _id not in _tags:
            _tags[_id] = []   
        
        _tags[_id].append(tag)


    regions = all_regions()
    _regions = {}
    for region in regions:
        
        _id = int(region['amiversion'])
        if _id not in _regions:
            _regions[_id] = []   
        
        _regions[_id].append(region)

    _versions = []
    for version in versions:
        _t = []
        try:
            _t = _tags[int(version['id'])]
        except:
            pass

        _r = []
        try:
            _r = _regions[int(version['id'])]
        except:
            pass

        _versions.append(formatted_row(
            version,
            _t,
            _r,
            -1
        ))

    return _versions
