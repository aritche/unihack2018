#!/usr/bin/python

# Import modules for CGI handling
import cgi 

base_url="test"
courses=[]

def main():
	# print the header and start the body
	print "Content-type:text/html\r\n\r\n"
	print """
	<html>
	<head>
            <link rel="stylesheet" href="courses.css" type="text/css"></style>
        </head>
	<body>
	"""
	

	searched = True
	form = cgi.FieldStorage()

	# if they haven't added a course yet
	if "searched_for" not in form:
		searched = False
	# if they have added a course
	else:
		# get all entered courses so far
		courses.append(form["searched_for"].value)
		if "prevCourse" in form:
			prevCourses = form["prevCourse"].value
			courses.extend(prevCourses.split(','))
			courses[-1] = courses[-1].replace('"', '')
		
		# check if they entered a mark
		if "mark" in form:
			mark = form["mark"].value
			print mark
		else:
			mark = ""

	searchBar()
	
	if searched == True:
		printSelectedCourses() 
		getRecords()

	# end the body and the html
	print """
	</body>
	</html>
	"""

def printSelectedCourses():
	print "<strong>COMPLETED SUBJECTS:</strong>"
	print "<div id=\"selected_courses\">"
	print "<ul>"
	for course in courses:
		print "<li>" + course + "</li>"
	print "</ul>"
	print "</div>"
	print "<hr>"

def getRecords():
	print "<strong>RECOMMENDATIONS</strong>"
	possible = getFuturePossibleCourses(courses)
	for item in possible[0]:
		print "<p>" + item + "</p>"
	for item in possible[1]:
		print "<p style=\"color:red\">" + item + "</p><br>"

# given a list of prereqs for a course, do taken courses satisfy these prereqs
def checkOptions(prereqs,taken):
	for course in prereqs:
		if "|" in course:
			conjunctions = course.split("|")
			flag = True
			for element in conjunctions:
				if element not in taken:
					flag = False
					break
			if flag is not False:
				return True
		else:
			if course in taken:
				return True
	return False
	

# given a list of prereqs for a course, do taken courses satisfy these prereqs
def checkOptions(prereqs,taken):
	for course in prereqs:
		if "|" in course:
			conjunctions = course.split("|")
			flag = True
			for element in conjunctions:
				if element not in taken:
					flag = False
					break
			if flag is not False:
				return True
		else:
			if course in taken:
				return True
	return False

def getFuturePossibleCourses(currentCourses):
	#matches is a list of the unit codes that are possibilities.
	#This list is filled as the code iterates
	matches = []
	noPrereqs = []
	#opens the file to read
	with open("db.txt","r") as file:
		#creates the object data which is the text file in a different format
		allCourses = file.readlines()
		#Does a for loop based on each line of the data
		for course in allCourses:
			#splits the course based on commas
			fields = course.split(",")
			unitCode = fields[0]
			unitName = fields[1]
			unitFaculty = fields[2]
			unitSchool = fields[3]
			prereqs = fields[4:]

			# if no prereqs, course is a match
			if len(prereqs) == 0:
				noPrereqs.append(course)
			# if exist prereqs, further process matches
			else:
				prereqs[-1] = prereqs[-1].strip('\n')
				if checkOptions(prereqs,currentCourses) == True:
					matches.append(course)
						
	if (len(matches)!=0):
		return [matches, noPrereqs]
		#return list(set(matches)) 
	else:	
		return [[], []]

def searchBar():
	print """	
		<div id="search_wrapper">
			<form id="search-form">
				<input class='search_bar' type="text" name="searched_for" placeholder="Enter a subject...">
				<select name="mark">
					<option value="HD">HD</option>
					<option value="D">D</option>
					<option value="C">C</option>
					<option value="P">P</option>
					<option value="FAIL">Fail</option>
				</select>
				<input type="submit" value="Add">
	"""
	print "<input type='hidden' name='prevCourse' value=" + (",").join(courses) + "\">" 

	print """
			</form>
		</div>
	"""


main()
