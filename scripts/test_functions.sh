#!/bin/sh

prepare_files_for_testing() {
	local test_name=$1

	tmpdir="$(readlink -f $(mktemp -d .testXXXXXX))"
	trap "rm -rf $tmpdir" EXIT

	if ! [ -z "${TEST_ONLY_INDEX+x}" ]; then
		echo "Running $test_name on files in index"
		git diff-index -z -r --cached --name-only --diff-filter=d HEAD |
		git checkout-index --prefix=$tmpdir/ -z --stdin
		cd $tmpdir
	elif ! [ -z "${TEST_ONLY_REV+x}" ]; then
		if [ "$TEST_ONLY_REV" = 1 ]; then
			TEST_ONLY_REV=HEAD
		fi

		echo "Running $test_name on files in HEAD"
		git archive $TEST_ONLY_REV | tar -C $tmpdir -xf -
		cd $tmpdir
	else
		echo "Running $test_name on files in working directory"
	fi
}
