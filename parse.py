#!/usr/bin/env python3

import json
import os
import string
import sys

def snarf_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as fdin:
            return json.loads(fdin.read())
    except:
        raise

def sanitize(st):
    try:
        st = ' '.join(st.split())
        return st.strip()
    except:
        return("(missing)")

class ProjectInfo(dict):
    def __init__(self, d):
        for k in d.keys():
            self[k] = d[k]
   
    @property
    def name(self):
        return sanitize(self.get('name', '(missing project name)'))

    @property
    def url(self):
        for k in ('html_url', 'homepage'):
            try:
                return sanitize(self.get(k))
            except:
                pass
        return("NO_URL")

    @property
    def description(self):
        return sanitize(self.get('description'))

    @property
    def size(self):
        total = 0
        for metric in ('dependent_repos_count', 'dependents_count', 'stargazers_count'):
            try:
                total += int(self.get(metric, 0))
            except:
                pass
        return total

    def __repr__(self):
        return("[%s](%s) %s (%d)" % (self.name, self.url, self.description, self.size))


class SearchResult(list):
    def __init__(self, d):
        try:
            for item in d['items']:
                self.append(ProjectInfo(item))
        except TypeError:
            for item in d:
                self.append(ProjectInfo(item))


if __name__ == '__main__':
    destination = sys.argv[1]
    keyword = os.path.basename(destination)
    for file in ("data/github/%s" % keyword, "data/libraries/%s" % keyword):
        info = SearchResult(snarf_json(file))
        for r in info:
            print("%s %s %s %d %s" % (keyword, r.url, r.name, r.size, r.description))

