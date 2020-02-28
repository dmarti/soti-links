#!/usr/bin/bash

trap popd EXIT
pushd $PWD &> /dev/null
cd $(dirname "$0")

fail() {
	echo $*
	exit 1
}

try_pass() {
	# try to get the key from the password manager
	which pass &> /dev/null && export LIBRARIES_API_KEY=$(pass libraries.io/APIKEY)
}

[ "x" != "x$LIBRARIES_API_KEY" ] || try_pass
[ "x" != "x$LIBRARIES_API_KEY" ] || fail "Set the environment variable"
./libraries.py | sort -u > libraries.md

