# coding: utf-8

import os
import json
from flask import request, Blueprint

from drawingboard.responses import badjson, success, baseresponse
from drawingboard.lib.ami_versions import create_base_version, create_version_version
from drawingboard.lib.ami_versions import all_bases, versions_for_base


blueprint = Blueprint(
    'rest_ami_versions', __name__,
    url_prefix='/rest/ami_versions'
)

@blueprint.route('/list/base',methods=['GET'])
def get_bases():
    try:
        
        bases = all_bases()

    except Exception as e:
        return baseresponse(
            success=False,
            message="Unable to load base",
            errors=str(e)
        )

    return baseresponse(
        success=True,
        message=bases
    )

@blueprint.route('/list/base/<base_id>',methods=['GET'])
def get_base_versions(base_id):
    try:
        
        versions = versions_for_base(base_id)

    except Exception as e:
        return baseresponse(
            success=False,
            message="Unable to load versions for base %s" % base_id,
            errors=str(e)
        )

    return baseresponse(
        success=True,
        message=versions
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
        
        template = int(data['template'])
        if not template or template <= 0:
            raise RuntimeError("A template ID is required")
                
        append_date = bool(data['append_date'])
        append_version = bool(data['append_version'])
        if data['tags']:
            tag_list = list(data['tags'])
        else:
            tag_list = []
        description = data['description']

    except Exception as e:
        return baseresponse(
            success=False,
            message="Bad data input",
            errors=str(e)
        )

    try:
       create_base_version(
        template=template,
        name=name,
        append_date=append_date,
        append_version=append_version,
        tags=tag_list,
        description=description
    )
    except Exception as e:
        return baseresponse(
            success=False,
            message="Unable to create ami version",
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

        template = int(data['template'])

        region_list = []
        if data['regions']:
            region_list = list(data['regions'])

        base_region = data['base_region'].strip()
        if not base_region:
            raise RuntimeError("A base region is required")
        
    except Exception as e:
        return baseresponse(
            success=False,
            message="Bad data input",
            errors=str(e)
        )

    try:
        create_version_version(
            parent=parent,
            template=template,
            base_region=base_region,
            regions=region_list
        )
    except Exception as e:
        return baseresponse(
            success=False,
            message="Unable to create ami version version",
            errors=str(e)
        )

    return success()