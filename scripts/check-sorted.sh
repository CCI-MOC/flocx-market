#!/bin/bash

normalize() {
	grep -E -v '^$|^#' $1
}

for file in "$@"; do
	echo "Checking if $file is sorted"
	if ! diff -u <(normalize $file) <(normalize $file | sort); then
		echo "ERROR: $file is not sorted"
		exit 1
	fi
done
