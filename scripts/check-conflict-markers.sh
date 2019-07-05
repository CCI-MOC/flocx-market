#!/bin/sh

tmpdir=$(mktemp -d precommitXXXXXX)
trap "rm -rf $tmpdir" EXIT

git checkout-index -a --prefix=$tmpdir/

(
cd $tmpdir
echo "Checking for conflict markers"
if find . -type f -print0 |
	xargs -0 grep -Hn -E '^(<{7}|>{7}|={7})( |$)'; then

	echo "ERROR: found conflict markers" >&2
	exit 1

fi
)
