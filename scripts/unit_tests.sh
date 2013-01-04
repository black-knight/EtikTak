#!/usr/bin/bash

prog=$'\
from EtikTakProject import settings\n\
from subprocess import call\n\
progs = [s[s.rfind(".")+1:len(s)] for s in settings.MY_APPS]\n\
print progs\n\
call(["./manage.py", "test"] + progs)\n\
'

python -c "$prog"

