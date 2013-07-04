#!/usr/bin/env python

import pip
from subprocess import call

for dist in pip.get_installed_distributions():
    call('pip install --upgrade ' + dist.project_name, shell=True)

call('pip freeze > requirements.txt', shell=True)

