# coding: utf-8

import sqlite3
from drawingboard.constants import AWS_REGIONS

sqlite3_conn = sqlite3.connect('/etc/drawingboard/sqllite.db',check_same_thread=False)
sqlite3_conn.row_factory = sqlite3.Row
sqlite3_conn.isolation_level = None

def init():
    sqlite3_conn.execute('PRAGMA encoding = "UTF-8";')

    sqlite3_conn.execute("""CREATE TABLE IF NOT EXISTS AWSRegions(
        id INTEGER PRIMARY KEY,
        name TEXT,
        region TEXT,
        UNIQUE(region) ON CONFLICT IGNORE
    )
    """)
    _init_aws_regions()

    sqlite3_conn.execute("""CREATE TABLE IF NOT EXISTS AMIVersionsRegions(
        id INTEGER PRIMARY KEY,
        region INT,
        amiversion INT,
        base BOOLEAN,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    sqlite3_conn.execute("""CREATE TABLE IF NOT EXISTS Tags(
        id INTEGER PRIMARY KEY,
        tag TEXT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(tag) ON CONFLICT IGNORE
    )
    """)

    sqlite3_conn.execute("""CREATE TABLE IF NOT EXISTS AMIVersionsTags(
        id INTEGER PRIMARY KEY,
        tag INT,
        amiversion INT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    sqlite3_conn.execute("""CREATE TABLE IF NOT EXISTS AminationTemplatesTags(
        id INTEGER PRIMARY KEY,
        tag INT,
        template INT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    sqlite3_conn.execute("""CREATE TABLE IF NOT EXISTS AminationTemplates(
        id INTEGER PRIMARY KEY,
        version INT,
        parent INT,
        name TEXT,
        description TEXT,
        provisioner TEXT,
        cli TEXT,
        append_date BOOLEAN,
        append_version BOOLEAN,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)


    sqlite3_conn.execute("""CREATE TABLE IF NOT EXISTS AMIVersions(
        id INTEGER PRIMARY KEY,
        version INT,
        parent INT,
        template INT,
        name TEXT,
        description TEXT,
        append_date BOOLEAN,
        append_version BOOLEAN,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    sqlite3_conn.execute("""CREATE TABLE IF NOT EXISTS Aminations(
        id INTEGER PRIMARY KEY,
        parent INT,
        version INT,
        name TEXT,
        description TEXT,
        cache_key TEXT,
        started BOOLEAN,
        template INT,
        amiversion INT,
        append_date BOOLEAN,
        append_version BOOLEAN,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

def _init_aws_regions():
    try:
        sqlite3_conn.execute("BEGIN TRANSACTION;")
        for region in AWS_REGIONS:
            sqlite3_conn.execute("INSERT INTO AWSRegions (`name`,`region`) VALUES (:name,:region)",
                {"name":region['name'],"region":region['region']}
            )
        sqlite3_conn.execute("COMMIT;")
    except Exception as e:
        sqlite3_conn.execute("ROLLBACK;")
        raise e

