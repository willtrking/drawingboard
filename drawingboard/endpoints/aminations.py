# coding: utf-8

from flask import Blueprint, render_template, request
from drawingboard.lib.aminations import all_base_aminations, load_base, aminations_for_base
from drawingboard.lib.aminations import load_version as load_amination_version
from drawingboard.lib.amination_templates import all_bases as all_template_bases
from drawingboard.lib.amination_templates import versions_for_base as template_versions_for_base
from drawingboard.lib.amination_templates import load_version as load_template_version
from drawingboard.lib.ami_versions import all_versions as all_ami_versions
from drawingboard.lib.ami_versions import versions_for_base as ami_versions_for_base
from drawingboard.lib.ami_versions import all_bases as all_ami_bases
from drawingboard.lib.ami_versions import load_base as load_base_ami_version
from drawingboard.lib.ami_versions import load_version as load_ami_version_version

blueprint = Blueprint('aminations', __name__, url_prefix='/')

@blueprint.route('aminations',methods=['GET'])
def aminations():
    template_bases = all_template_bases()
    template_map = {}

    for template in template_bases:
        template_map[template['id']] = template

    ami_bases = all_ami_bases()
    ami_map = {}
    
    for ami in ami_bases:
        ami_map[ami['id']] = ami


    return render_template(
        'aminations/aminations.j2',
        aminations=all_base_aminations(),
        template_map=template_map,
        ami_map=ami_map,
        ami_bases=ami_bases
    )

@blueprint.route('aminations/amination/<base>',methods=['GET'])
def amination(base):
    base_info=load_base(base)
    ami_versions = ami_versions_for_base(base_info['amiversion'])

    ami_map = {}
    for version in ami_versions:
        ami_map[version['id']] = version

    return render_template(
        'aminations/amination.j2',
        base_info=base_info,
        aminations=aminations_for_base(base),
        ami_map=ami_map,
        base_ami=load_base_ami_version(base_info['amiversion'])
    )


@blueprint.route('aminations/amination/<base>/<version>',methods=['GET'])
def amination_version(base,version):
    base_info=load_base(base)
    version_info = load_amination_version(base,version)
    ami_version = load_ami_version_version(base_info['amiversion'],version_info['amiversion'])
    template_version = load_template_version(base_info['template'],version_info['template'])

    return render_template(
        'aminations/amination_version.j2',
        base_info=base_info,
        version_info=version_info,
        ami_version=ami_version,
        template_version=template_version
    )


@blueprint.route('aminations/amination/<base>/<version>/stdout',methods=['GET'])
def stdout(base,version):
    version_info = load_amination_version(base,version)

    return render_template(
        'aminations/std.j2',
        type='STDOUT',
        version_info=version_info
    )

@blueprint.route('aminations/amination/<base>/<version>/stderr',methods=['GET'])
def stderr(base,version):
    version_info = load_amination_version(base,version)

    return render_template(
        'aminations/std.j2',
        type='STDERR',
        version_info=version_info
    )


