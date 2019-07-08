#!/bin/sh

TOP=$(git rev-parse --show-toplevel)
. $TOP/scripts/test_functions.sh

prepare_files_for_testing "check for conflict markers"

if find . -name .tox -prune -o -type f -print0 |
	xargs -0 grep -Hn -E '^(<{7}|>{7}|={7})( |$)'; then

	echo "ERROR: found conflict markers" >&2
	exit 1
fi
