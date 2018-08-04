#!/usr/bin/python

import CGI

header = '''
Content-type:text/html\r\n\r\n
<html>
<head>
<title>Clever Course</title>
</head>
'''
print header

print '<body>'
file="hi"
print '<h2>' + file + ' </h2>'

searchBar = '''
<div id="searchBar">
		
		<a class="active" href="#home">Home</a>
		<a href="#profile">Profile</a>
		<a href="#recommend">Recommendations</a>
'''
print searchBar

print '</body>'
print '</html>'

