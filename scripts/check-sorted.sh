#!/bin/bash

normalize() {
	grep -E -v '^$|^#' $1
}

TOP=$(git rev-parse --show-toplevel)
. $TOP/scripts/test_functions.sh

prepare_files_for_testing "check for sorted"

for file in "$@"; do
	[ -f "$file" ] || continue

	echo "Checking if $file is sorted"
	if ! diff -u <(normalize $file) <(normalize $file | sort); then
		echo "ERROR: $file is not sorted"
		exit 1
	fi
done
