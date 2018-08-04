#!/usr/bin/python

import CGI

header = '''
Content-type:text/html\r\n\r\n"
'<html>'
'<head>'
'<title>Clever Course</title>'
'</head>'
'''
print header

print '<body>'
file="hi"
print '<h2>' + file + ' </h2>'

print '</body>'
print '</html>'

