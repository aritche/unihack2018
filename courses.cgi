#!/usr/bin/python

# Import modules for CGI handling
import cgi 

base_url="test"

def main():
	# print the header and start the body
	print "Content-type:text/html\r\n\r\n"
	print """
	<html>
	<head><link rel="stylesheet" href="courses.css" type="text/css"></style></head>
	<body>
	"""
	
	searchBar()

	form = cgi.FieldStorage()
	if "searched_for" not in form:
		print "Search for something"
	else:
		course = form["searched_for"].value
		getRecords(course)

	# end the body and the html
	print """
	</body>
	</html>
	"""

def getRecords(course):
	with open("db.txt") as f:
		lines = f.readlines()
		for line in lines:
			if course in line:
				print line + "<br>"

def searchBar():
	print """	
		<form id="search-form">
			<input class='search_bar' type="text" name="searched_for">
			<input id='search_button' type="submit" value="Search">
		</form>
	"""

main()
