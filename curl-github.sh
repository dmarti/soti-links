#!/usr/bin/bash

set -e
set -x

outdir=$(dirname $1)
mkdir -p $outdir

keyword=$(basename $1)

curl --silent --output $1 \
	-H "Accept: application/vnd.github.mercy-preview+json" \
	https://api.github.com/search/repositories?q=topic:$keyword \

