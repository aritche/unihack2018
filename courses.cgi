#!/usr/bin/python

# Import modules for CGI handling
import cgi 
import re

base_url="test"
courses=[]
marks=[]

coursesInfo=[] # complete records of a course

def main():
	# print the header and start the body
	print "Content-type:text/html\r\n\r\n"
	print """
	<html>
	<head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
            <link rel="stylesheet" href="courses.css" type="text/css"></style>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
            <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/jc/bootstrap.min.js"></script>
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
		if "prevCourses" in form:
			prevCourses = form["prevCourses"].value
			courses.extend(prevCourses.split(','))
			courses[-1] = courses[-1].replace('"', '')
		
		# check if they entered a mark
		if "mark" in form:
			marks.append(form["mark"].value)
			if "prevMarks" in form:
				prevMarks = form["prevMarks"].value
				marks.extend(prevMarks.split(','))
				marks[-1] = marks[-1].replace('"', '')

	getInfo()
	filterCourses()
	searchBar()

	if searched == True:
		printSelectedCourses() 
		getRecords()

	# end the body and the html
	print """
	</body>
	</html>
	"""

# filter courses in the course list to existing courses
def filterCourses():
	newCourses = []
	for course in courses:
		course = course.upper()
		if not re.match(r"^[A-Z]{4}[0-9]{4}$", course):
			continue	
		newCourses.append(course)
	courses[:] = newCourses

# given a list of db records, sort them by rank
def rankCourses(records):
	ranked = []
	for record in records:
		ranked.append([record, getRank(record)])
	ranked = sorted(ranked, key=lambda x: x[1], reverse=True)
	
	rankedWithoutScore = []
	# remove rank value
	for item in ranked:
		rankedWithoutScore.append(item[0])
	return rankedWithoutScore

# return a rank for a given course record from the db
# rank depends on completed courses
def getRank(courseRecord):
	courseRecord = courseRecord.split(',')
	school = courseRecord[3]

	# how many times has the student completed courses from this school
	score = 0
	for course in coursesInfo:
		fields = course.split(',')
		completedSchool = fields[3]
		if school == completedSchool:
			score += 1

	return score

# populate coursesInfo array with complete info on a course
def getInfo():
	with open("db.txt", "r") as file:
		allCourses = file.readlines()
		# for completed course
		for completedCourse in courses:
			for courseEntry in allCourses:
				fields = courseEntry.split(",")
				unitCode = fields[0]
				if completedCourse == unitCode:
					coursesInfo.append(courseEntry)
					break


def printSelectedCourses():
	print """
            <div class="container">
                <strong>COMPLETED SUBJECTS:</strong>
                <table class="table table-dark table-hover">
                    <thead>
                        <tr>
                            <th>Marks</th>
                            <th>Course</th>
                        </tr>
                    </thead>
                    <tbody>
        """
	for x in range(0,len(courses)):
                print "<tr>"
                print "<td>" + marks[x] + "</td>"
		print "<td>" + courses[x] + "</td>"
                print "</tr>"
	print "</tbody>"
        print "</table>"
	print "</div>"
	print "<hr>"

def getRecords():
        print """
            <div class="container">
	        <strong>RECOMMENDED</strong>
                <table class="table table-dark table-hover">
                    <thead>
                        <tr>
                            <th>Course</th>
                            <th>Information</th>
                        </tr>
                    </thead>
                    <tbody>
        """

	possible = getFuturePossibleCourses()

	possible[0] = rankCourses(possible[0])
	possible[1] = rankCourses(possible[1])
	

	for item in possible[0]:
                splitItem=item.split(',')
                print "<tr>"
		print "<td><a href='http://www.handbook.unsw.edu.au/undergraduate/courses/2018/" + splitItem[0] + ".html'>"+ splitItem[0] + "</a></td>"
		print "<td>" + splitItem[1] + "</td>"
                print "<td>"
                for x in range(2,4):
			print splitItem[x]
                print "</td>"
                print "</tr>"
        print """
                </tbody>
                <table class="table table-dark table-hover">
                    <tbody>
        """

	"""
	for item in possible[1]:
                splitItem=item.split(',')
                print "<tr>"
		print "<td><a style='color:red'href='http://www.handbook.unsw.edu.au/undergraduate/courses/2018/" + splitItem[0] + ".html'>"+ splitItem[0] + "</a></td>"
		print "<td style='color:red'>" + splitItem[1] + "</td>"
                print "<td><p style=\"color:red\">" 
                for x in range(2,4):
                    print splitItem[x]
                print "</p></td>"
                print "</tr>"
	"""
        
	print "</tbody>"
        print "</table>"
        print "</div>"

def bandToMark(band):
	if grade == "HD":
		return 1	
	elif grade == "D":
		return 0.7
	elif grade == "C":
		return 0.4
	elif grade == "P":
		return 0.1
	else:
		return 0

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
				element = element.replace("(", "")
				element = element.replace(")", "")
				if element not in taken:
					flag = False
					break
			if flag is not False:
				return True
		else:
			if course in taken:
				return True
	return False

def getFuturePossibleCourses():
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
				if checkOptions(prereqs,courses) == True:
					matches.append(course)
				
	# don't recommend courses that you've already taken		
	for course in courses:
		for match in matches:
			if match.split(',')[0] == course:
				matches.remove(match)
		for match in noPrereqs:
			if match.split(',')[0] == course:
				noPrereqs.remove(match)

	if (len(matches)!=0):
		return [matches, noPrereqs]
		#return list(set(matches)) 
	else:	
		return [[], []]

def searchBar():
        print """
                <div class="container">
                <div class="jumbotron">
                    <h1>Clever Course</h1>
                </div>
                <nav class="navbar navbar-expand-md bg-dark navbar-dark">
			<p style="font-size: 18px;">Please enter courses you have completed:</p>
			<form class="form-inline" id="search-form">
				<input class="form-control mr-sm-2 type="text" name="searched_for" placeholder="Subject Code">
				<select name="mark">
					<option value="HD">HD</option>
					<option value="D">D</option>
					<option value="C">C</option>
					<option value="P">P</option>
					<option value="FAIL">Fail</option>
				</select>
				<button class="btn btn-success" type="submit" value="Add">Add</button>
	"""
	print "<input type='hidden' name='prevCourses' value='" + (",").join(courses) + "'>"
	print "<input type='hidden' name='prevMarks' value='" + (",").join(marks) + "'>"
	print """
			</form>
		</nav>
                </div>
	"""

main()
