#!/usr/bin/env python3

from datetime import datetime
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
        result = "<tr><td><b><a href='%s'>%s</a>:</b>&nbsp;%s</td><td>%d</td>" % (self.url, self.name, self.description, self.totalscore)
        for j in keywords: 
            try:
                result += "<td>%d</td>" % scores[self.url][j]
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

for line in sys.stdin:
    try:
        (keyword, url, name, score, description) = line.split(' ', 4)
    except ValueError:
        print(line, file=sys.stderr)
        raise
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

if (format == 'html'):
    print('<html><head><title>Results</title><style type="text/css">')
    print(tablestyle)

    print('</style></head><body><table><tr><th>Project</th><th>Total score</th>')
    for w in keywords:
        print("<th>%s</th>" % w)
    print("</tr>")

    for r in rows:
        print(r.as_html())
    print('</table><p>Built %s (<a href="results.csv" target="_blank">(CSV version for spreadsheets)</a></p></html>' % datetime.now())
else: # CSV version
    sys.stdout.write('"Name","URL","Description","Total score"')
    for w in keywords:
        sys.stdout.write(',"%s"' % w)
    sys.stdout.write("\n")
    for r in rows:
        sys.stdout.write(r.as_csv())

