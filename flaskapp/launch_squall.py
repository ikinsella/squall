#!/usr/bin/env python

import subprocess

subprocess.Popen(['mongod', '--dbpath', '/data/db'])
subprocess.Popen(['./manage.py', 'server'])
