#!/usr/bin/env python3

import sys

class TableRow(object):
    def __init__(self, url, name, description, totalscore, scores):
        self.url = url
        self.name = name
        self.description = description
        self.totalscore = totalscore
        self.scores = []
        for w in keywords:
            try:
                self.scores.append(scores[url][w])
            except KeyError:
                self.scores.append(0)

    def __lt__(self, other):
        return self.totalscore < other.totalscore

    def as_html(self):
        result = "<tr><td><a href='%s'>%s</a></td><td>%s</td><td>%d</td>" % (self.url, self.name, self.description, self.totalscore)
        for j in keywords: 
            try:
                result += "<td>%d</td>" % scores[self.url][j]
            except KeyError:
                result += "<td></td>"
        result += "</tr>"
        return result


scores = {}
totalscore = {}
names = {}
descriptions = {}
keywords = {}
for line in sys.stdin:
    (keyword, url, name, score, description) = line.split(' ', 4)
    keywords[keyword] = 1
    try:
        scores[url][keyword] = int(score)
        totalscore[url] += int(score)
    except KeyError:
        scores[url] = {keyword: int(score)}
        totalscore[url] = int(score)
    names[url] = name
    descriptions[url] = description

keywords = list(keywords.keys())
keywords.sort()
rows = []
for k in names.keys():
    rows.append(TableRow(k, names[k], descriptions[k], totalscore[k], scores))

rows.sort(reverse=True)

print('<html><body><table border=1><tr><th colspan="2">Project</th><th>Total score</th>')
for w in keywords:
    print("<th>%s</th>" % w)
print("</tr>")

for r in rows:
    print(r.as_html())
print("</table></html>")
    
