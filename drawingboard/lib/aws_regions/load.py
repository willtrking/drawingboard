# coding: utf-8

from drawingboard.db import sqlite3_conn    

def retrieve_regions(regions,require_all=True):
    _regions = []
    for region in set(regions):
        _region = sqlite3_conn.execute("SELECT * FROM AWSRegions WHERE region = :region LIMIT 1;",{"region":region}).fetchone()
        if not _region and require_all:
            raise RuntimeError("Missing region %s" % region)
                
        if _region:
            _regions.append(_region)

    return _regions