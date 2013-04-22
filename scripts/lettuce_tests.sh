#!/usr/bin/bash

./manage.py sqlclear clients products supermarkets | ./manage.py dbshell
./manage.py syncdb

./manage.py harvest features

