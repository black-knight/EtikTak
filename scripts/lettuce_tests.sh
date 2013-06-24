#!/usr/bin/bash

./manage.py sqlclear clients products stores | ./manage.py dbshell
./manage.py syncdb

./manage.py harvest features

