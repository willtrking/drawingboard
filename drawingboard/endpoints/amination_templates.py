# coding: utf-8

import json
from flask import Blueprint, redirect, render_template, request, g

from drawingboard.lib.amination_templates import all_bases, versions_for_base, load_base, tags_for_template
from drawingboard.lib.tags import all_tags

blueprint = Blueprint('amination_templates', __name__, url_prefix='/')

@blueprint.route('amination_templates',methods=['GET'])
def templates():
    templates = all_bases()
    return render_template(
        'amination_templates/templates.j2',
        templates=templates,
        tags=all_tags()
    )

@blueprint.route('amination_templates/<base>',methods=['GET'])
def template(base):
    base_info = load_base(base)
    versions = versions_for_base(base)
    return render_template(
        'amination_templates/template.j2',
        base_info=base_info,
        versions=versions
    )
