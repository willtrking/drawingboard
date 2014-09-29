# coding: utf-8

from flask import Blueprint, redirect, render_template, request, g

from drawingboard.constants import AWS_REGIONS
from drawingboard.lib.amination_templates import versions_for_base as versions_for_templates
from drawingboard.lib.amination_templates import all_bases as all_templates
from drawingboard.lib.amination_templates import load_base as load_base_template
from drawingboard.lib.ami_versions import all_bases, load_base
from drawingboard.lib.tags import all_tags


blueprint = Blueprint('ami_versions', __name__, url_prefix='/')

@blueprint.route('ami_versions',methods=['GET'])
def versions():
    templates = all_templates()
    versions = all_bases()
    return render_template(
        'ami_versions/versions.j2',
        versions=versions,
        templates=templates,
        tags=all_tags()
    )

@blueprint.route('ami_versions/<base>',methods=['GET'])
def version(base):
    base_info = load_base(base)
    templates = versions_for_templates(base_info['template'])

    template_map = {}
    for template in templates:
        template_map[template['id']] = template
    template_map[base_info['template']] = load_base_template(base_info['template'])

    region_map = {}
    for region in base_info['regions']:
        region_map[region['region']] = True

    return render_template(
        'ami_versions/version.j2',
        base_info=base_info,
        template_map=template_map,
        regions=AWS_REGIONS,
        region_map=region_map
    )
