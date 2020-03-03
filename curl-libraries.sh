#!/usr/bin/bash

set -e
set -x

fail() {
	echo $*
	exit 1
}

try_pass() {
	# try to get the key from the password manager
	which pass &> /dev/null && export LIBRARIES_API_KEY=$(pass libraries.io/APIKEY)
}

[ "x" != "x$LIBRARIES_API_KEY" ] || try_pass
[ "x" != "x$LIBRARIES_API_KEY" ] || fail "LIBRARIES_API_KEY environment variable not set"

outdir=$(dirname $1)
mkdir -p $outdir
keyword=$(basename $1)

# API key is required.
curl --silent --output $1 \
	"https://libraries.io/api/search?q=$keyword&api_key=$LIBRARIES_API_KEY"

