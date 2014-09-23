# coding: utf-8

from flask import jsonify


def baseresponse(success,message,errors=[]):
    if not isinstance(errors,list):
        errors = [errors]

    return jsonify(
        success=success,
        message=message,
        errors=errors
    )

def success():
    return baseresponse(
        success=True,
        message="OK"
    )

def badjson():
    return baseresponse(
        success=False,
        message="Bad JSON input"
    )