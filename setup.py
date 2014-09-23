# coding: utf-8

import sys, os, errno, shutil, stat
from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib

from drawingboard import __version__, constants

try:
    if sys.argv[1] == 'install':
        def mkdir_p(path):
            try:
                os.makedirs(path)
            except OSError as exc: # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else: raise

        mkdir_p('/etc/drawingboard/')
        mkdir_p('/etc/drawingboard/bin')
        mkdir_p('/etc/drawingboard/aminations/')
        _dir = os.path.dirname(os.path.realpath(constants.__file__))
        shutil.copy(_dir+'/bin/drawingboard_amination','/etc/drawingboard/bin')
        
        st = os.stat('/etc/drawingboard/bin')
        os.chmod('/etc/drawingboard/bin', st.st_mode | stat.S_IEXEC)

except IndexError: pass

setup(
    name = 'drawingboard',
    version = __version__,
    description = 'Web UI for Netflix aminator',
    author = 'William King',
    author_email = 'willtrking@gmail.com',
    zip_safe = False,
    include_package_data = True,
    packages=find_packages(),
    requires=['flask','dogpile.cache'],
    entry_points="""
    [console_scripts]
    drawingboard=drawingboard.app:start
    """
)