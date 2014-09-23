# coding: utf-8

from .formatting import formatted_row
from drawingboard.db import sqlite3_conn

def all_aminations():
    with sqlite3_conn:
        bases = sqlite3_conn.execute("SELECT * FROM Aminations ORDER BY id,created ASC").fetchall()

    _bases = []
    for base in bases:

        _bases.append(formatted_row(
            base
        ))

    return _bases


def load(amination):
    with sqlite3_conn:
        base = sqlite3_conn.execute("SELECT * FROM Aminations WHERE id = :amination LIMIT 1;",
            {"amination":amination}
        ).fetchone()

    return formatted_row(base)