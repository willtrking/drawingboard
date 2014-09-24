# coding: utf-8

import json
from flask import request, Blueprint

from drawingboard.responses import badjson, success, baseresponse
from drawingboard.lib.aminations import create_base_amination, create_amination_version
from drawingboard.lib.aminations import all_base_aminations, start_amination

blueprint = Blueprint(
    'rest_aminations', __name__,
    url_prefix='/rest/aminations'
)

@blueprint.route('/list/base',methods=['GET'])
def get_bases():
    try:
        
        bases = all_base_aminations()

    except Exception as e:
        return baseresponse(
            success=False,
            message="Unable to load aminations",
            errors=str(e)
        )

    return baseresponse(
        success=True,
        message=bases
    )

@blueprint.route('/run/<amination>',methods=['POST'])
def run(amination):

    start_amination(amination)

    return baseresponse(
        success=True,
        message=bases
    )

@blueprint.route('/create/base',methods=['PUT','POST'])
def create_base():
    try:
        data = request.get_json(force=True)
    except:
        return badjson()

    try:
        name = data['name'].strip()
        if not name:
            raise RuntimeError("Name is required")
        
        description = data['description']

        ami_version_base = int(data['ami_version_base'])
        if not ami_version_base or ami_version_base <= 0:
            raise RuntimeError("Bad base ami version id %s" % (ami_version_base))

    except Exception as e:
        return baseresponse(
            success=False,
            message="Bad data input",
            errors=str(e)
        )

    try:
        create_base_amination(
            name=name,
            description=description,
            ami_version_base=ami_version_base
        )
    except Exception as e:
        return baseresponse(
            success=False,
            message="Unable to create amination",
            errors=str(e)
        )

    return success()



@blueprint.route('/create/version',methods=['PUT','POST'])
def create_version():
    try:
        data = request.get_json(force=True)
    except:
        return badjson()

    try:

        parent = int(data['parent'])
        if not parent or parent <= 0:
            raise RuntimeError("Bad parent id %s" % (parent))

        ami_version = int(data['ami_version'])
        if not ami_version or ami_version <= 0:
            raise RuntimeError("Bad ami version id %s" % (ami_version))

        start = False
        if 'start' in data:
            start = bool(data['start'])


    except Exception as e:
        return baseresponse(
            success=False,
            message="Bad data input",
            errors=str(e)
        )

    try:
        create_amination_version(
            amination_base=parent,
            ami_version=ami_version,
            start=start
        )
    except Exception as e:
        return baseresponse(
            success=False,
            message="Unable to create amination",
            errors=str(e)
        )

    return success()
