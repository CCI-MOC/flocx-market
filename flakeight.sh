#!/bin/bash
# A simple wrapper around flake8 which makes it possible
# to ask it to only verify files changed in the current
# git HEAD patch.
#
# Intended to be invoked via tox:
#
#   tox -epep8 -- -HEAD
#
echo "Running flake8 on flocx_market"
exec python3 -m flake8 "flocx_market"
