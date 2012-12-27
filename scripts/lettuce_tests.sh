#!/usr/bin/bash

./manage.py reset --noinput clients products supermarkets users
./manage.py harvest features

