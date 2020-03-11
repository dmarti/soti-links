#!/usr/bin/env python3

from datetime import datetime
from math import log
import re
import sys

tablestyle = '''
* {
  font-family: sans-serif;
}
table {
  border: 1px solid #1C6EA4;
  background-color: #EEEEEE;
  text-align: left;
  border-collapse: collapse;
}
table td, table.s th {
  border: 1px solid #AAAAAA;
  padding: 3px 2px;
  vertical-align: bottom;
}
th {
  vertical-align: bottom;
}
table tr:nth-child(even) {
  background: #D0E4F5;
}
table thead {
  background: #1C6EA4;
  background: -moz-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
  background: -webkit-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
  background: linear-gradient(to bottom, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
  border-bottom: 2px solid #444444;
}
table thead th {
  font-weight: bold;
  color: #FFFFFF;
  border-left: 2px solid #D0E4F5;
}
table thead th:first-child {
  border-left: none;
}

table tfoot {
  font-weight: bold;
  color: #FFFFFF;
  background: #D0E4F5;
  background: -moz-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
  background: -webkit-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
  background: linear-gradient(to bottom, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
  border-top: 2px solid #444444;
}
table tfoot .links {
  text-align: right;
}
table tfoot .links a{
  display: inline-block;
  background: #1C6EA4;
  color: #FFFFFF;
  padding: 2px 8px;
  border-radius: 5px;
}
'''

def weight(keyword, scores):
    projects = scores.keys()
    match_count = 0
    for k in projects:
        try:
            tmp = scores[k][keyword]
            match_count += 1
        except KeyError:
            pass
    # print("keyword %s occurs %d times in %d projects" % (keyword, match_count, len(projects)))
    return log(len(projects) / match_count)

class TableRow(object):
    def __init__(self, url, name, description, totalscore, scores):
        self.url = url
        self.name = name
        self.description = description
        self.totalscore = totalscore
        self.scores = []

    def __lt__(self, other):
        return self.totalscore < other.totalscore

    def as_html(self):
        result = "<tr><td><b><a href='%s'>%s</a>:</b>&nbsp;%s</td><td>%s</td>" % (self.url, self.name, self.description, self.totalscore)
        for j in keywords: 
            try:
                s = round(scores[self.url][j] * weight(j, scores), 1)
                if not s:
                    s = ''
                result += "<td>%s</td>" % s
            except KeyError:
                result += "<td></td>"
        result += "</tr>"
        return result

    def as_csv(self):
        # Filter out special characters from description
        allowed = re.compile('[^a-zA-Z.(),/]')
        fd = allowed.sub(' ', self.description)
        fd = ' '.join(fd.split())
        result='"%s","%s","%s","%s"' % (self.name, self.url, fd, self.totalscore)
        for j in keywords:
            try:
                result += ',"%s"' % scores[self.url][j]
            except KeyError:
                result += ',""'
        result += "\n"
        return result

scores = {}
totalscore = {}
names = {}
descriptions = {}
keywords = {}

format = sys.argv[1]

def clean_kw(w):
    return (' ').join(w.split('+'))

for line in sys.stdin:
    try:
        (keyword, url, name, score, description) = line.split(' ', 4)
    except ValueError:
        print("Unexpected line: %s" % line, file=sys.stderr)
    keywords[keyword] = 1
    try:
        score = max(10, int(score))
    except:
        score = 10
    score = round(log(score, 10), 1)

    try:
        scores[url][keyword] = score
        totalscore[url] += score
        totalscore[url] = round(totalscore[url], 1)
    except KeyError:
        scores[url] = {keyword: score}
        totalscore[url] = score
    except ValueError:
        pass
    names[url] = name
    descriptions[url] = description

for url in names.keys():
    totalscore[url] = 0
    for keyword in keywords.keys():
        try:
            totalscore[url] += scores[url][keyword] * weight(keyword, scores)
        except KeyError:
            pass
    totalscore[url] = round(totalscore[url], 1)

keywords = list(keywords.keys())
keywords.sort()
rows = []
for k in names.keys():
    rows.append(TableRow(k, names[k], descriptions[k], totalscore[k], scores))

rows.sort(reverse=True)

if (format == 'html'):
    print('<html><head><title>Results</title><style type="text/css">')
    print(tablestyle)

    print('</style></head><body><table><tr><th>Project</th><th>Total score</th>')
    for w in keywords:
        print("<th>%s</th>" % clean_kw(w))
    print("</tr>")

    for r in rows:
        if not 'http' in r.url:
            continue
        print(r.as_html())
    print('</table><p>Built %s <a href="results.csv" target="_blank">(CSV version for spreadsheets)</a></p></html>' % datetime.now())
else: # CSV version
    sys.stdout.write('"Name","URL","Description","Total score"')
    for w in keywords:
        sys.stdout.write(',"%s"' % clean_kw(w))
    sys.stdout.write("\n")
    for r in rows:
        if not 'http' in r.url:
            continue
        sys.stdout.write(r.as_csv())

