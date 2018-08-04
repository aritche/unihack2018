#!/usr/bin/python

# Import modules for CGI handling
import CGI

# Create instance of FieldStorage
form = CGI.FieldStorage()

# Get data from fields
search = form.getvalue('search')

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
		<form action="file name here" method="post">
			<input type="text" name="search"/>
			<input type="submit" value="submit"/>
		</form>
'''
print searchBar

print '</div>'

print '</body>'
print '</html>'

