#!/usr/bin/env python3

import json
import os
import requests

keywords = ['ccpa', 'gdpr']

class ProjectInfo(dict):
    def __init__(self, d):
        for k in d.keys():
            self[k] = d[k]
    
    def __repr__(self):
        try:
            description = ' '.join(self['description'].split())
        except AttributeError:
            description = ''
        total = self['forks'] + self['dependent_repos_count'] + self['dependents_count']
        return(" * [%s](%s) %s (%s) %d" % (self['name'], self['repository_url'], description, ' '.join(self['keywords']), total))

result = []
for word in keywords:

    url = "https://libraries.io/api/search?q=%s&api_key=%s" % (word, os.environ.get('LIBRARIES_API_KEY'))
    text = requests.get(url).text
    info = json.loads(text)

    for item in info:
        result.append(ProjectInfo(item))
        
print("\n".join([r.__repr__() for r in result]))

