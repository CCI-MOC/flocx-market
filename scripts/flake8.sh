#!/bin/bash

TOP=$(git rev-parse --show-toplevel)
. $TOP/scripts/test_functions.sh

prepare_files_for_testing "flake8"

python3 -m flake8 "$@"
