#!/usr/bin/bash

outdir=$(dirname $1)
mkdir -p $outdir

keyword=$(basename $1)

curl -H "Accept: application/vnd.github.mercy-preview+json" \
	https://api.github.com/search/repositories?q=topic:$keyword \
> $1

