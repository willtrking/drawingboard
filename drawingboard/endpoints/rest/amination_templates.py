# coding: utf-8

import json
from flask import request, Blueprint

from drawingboard.responses import badjson, success, baseresponse
from drawingboard.lib.amination_templates import create_base_template, create_template_version
from drawingboard.lib.amination_templates import all_bases, versions_for_base


blueprint = Blueprint(
    'rest_amination_templates', __name__,
    url_prefix='/rest/amination_templates'
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
        
        append_version = bool(data['append_version'])
        append_date = bool(data['append_date'])
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
        create_base_template(
            name=name,
            append_date=append_date,
            append_version=append_version,
            tags=tag_list,
            description=description,
            provisioner='',
            cli_args=[]
        )
    except Exception as e:
        return baseresponse(
            success=False,
            message="Unable to create template",
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

        aminator_provsioner = data['provisioner']
        if not aminator_provsioner:
            raise RuntimeError("Provisioner is required")

        cli_args = []
        for arg in data['cli_args']:
            cli_args.append({
                'name' : arg['name'],
                'value' : unicode(arg['value'])
            })

    except Exception as e:
        return baseresponse(
            success=False,
            message="Bad data input",
            errors=str(e)
        )

    try:
        create_template_version(
            parent=parent,
            provisioner=aminator_provsioner,
            cli_args=cli_args
        )
    except Exception as e:
        return baseresponse(
            success=False,
            message="Unable to create template version",
            errors=str(e)
        )

    return success()