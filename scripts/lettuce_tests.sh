#!/usr/bin/bash

./manage.py reset --noinput clients products supermarkets
./manage.py harvest features

