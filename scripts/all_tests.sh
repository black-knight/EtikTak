#!/usr/bin/bash

set -e

./scripts/unit_tests.sh
./scripts/lettuce_tests.sh
