# coding: utf-8

import json
from flask import request, Blueprint

from drawingboard.responses import badjson, success, baseresponse
from drawingboard.lib.aminations import create_amination, all_aminations, start_amination

blueprint = Blueprint(
    'rest_aminations', __name__,
    url_prefix='/rest/aminations'
)

@blueprint.route('/list',methods=['GET'])
def get_bases():
    try:
        
        bases = all_aminations()

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

@blueprint.route('/create',methods=['PUT','POST'])
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
        ami_version = int(data['ami_version'])
        if not ami_version or ami_version <= 0:
            raise RuntimeError("Bad ami version id %s" % (ami_version))

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
        create_amination(
            name=name,
            description=description,
            ami_version=ami_version,
            ami_version_base=ami_version_base
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return baseresponse(
            success=False,
            message="Unable to create amination",
            errors=str(e)
        )

    return success()
