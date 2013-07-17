#!/usr/bin/env python

import os
import sys

envkeys = ['FRED_API_KEY']

for key in envkeys:
    setattr(sys.modules[__name__], key, os.environ.get(key, None))

FRED_API_KEY = '34a7386da77efa763957d30a167376aa'


