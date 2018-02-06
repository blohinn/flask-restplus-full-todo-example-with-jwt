import tempfile

import os

basedir = os.path.abspath(os.path.dirname(__file__))

a = tempfile.mktemp(dir=basedir, suffix='.db')

print(a)