#!/usr/bin/env python

import os
import subprocess
import sys

if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'
subprocess.call(["pip", "install", 'pep8'])
