# coding: utf-8

from flask import Blueprint, render_template, request
from drawingboard.lib.aminations import all_aminations
from drawingboard.lib.amination_templates import all_versions as all_template_versions
from drawingboard.lib.ami_versions import all_versions as all_ami_versions
from drawingboard.lib.ami_versions import all_bases as all_ami_bases

blueprint = Blueprint('aminations', __name__, url_prefix='/')

@blueprint.route('aminations',methods=['GET'])
def aminations():
    template_versions = all_template_versions()
    template_map = {}

    for template in template_versions:
        template_map[template['id']] = template

    ami_versions = all_ami_versions()
    ami_map = {}
    
    for ami in ami_versions:
        ami_map[ami['id']] = ami

    return render_template(
        'aminations/aminations.j2',
        aminations=all_aminations(),
        template_map=template_map,
        ami_map=ami_map,
        ami_bases=all_ami_bases()
    )

@blueprint.route('aminations/amination/<base>',methods=['GET'])
def amination(base):
    
    return render_template('aminations/amination.j2')
