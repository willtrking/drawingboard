# coding: utf-8

from drawingboard.db import sqlite3_conn

def add_tags(tags,conn=None):
    if not isinstance(tags,list):
        tags = [tags]

    _args = []
    for tag in tags:
        _args.append(
            (tag,)
        )
    if not conn:
        try:
            sqlite3_conn.execute("BEGIN TRANSACTION;")
            sqlite3_conn.executemany(
                "INSERT INTO Tags(`tag`) VALUES (?)",_args)
            sqlite3_conn.execute("COMMIT;")
        except Exception as e:
            sqlite3_conn.execute("ROLLBACK;")
            raise e

    else:
        conn.executemany("INSERT INTO Tags(`tag`) VALUES (?)",_args)

