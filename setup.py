#!/usr/bin/env python
import os
import subprocess
import sys


if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'

subprocess.call(["pip", "install", 'pep8'])
subprocess.call(["pip", "install", 'mysql-python'])
subprocess.call(["pip", "install", 'flask'])]
subprocess.call(["pip", "install", 'SQLAlchemy'])
subprocess.call(["pip", "install", 'Flask-SQLAlchemy'])
#subprocess.call(["mysql"
