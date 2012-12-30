#!/usr/bin/bash
find . -name "*.py" | xargs grep -L "Copyright (c) 2012, Daniel Andersen (dani_ande@yahoo.dk)"
