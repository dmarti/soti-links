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

outdir=$(dirname $1)
mkdir -p $outdir
keyword=$(basename $1)

curl --output $1 https://libraries.io/api/search?q=$keyword&api_key=$LIBRARIES_API_KEY

