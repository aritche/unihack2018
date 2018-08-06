#!/usr/bin/python

# Import modules for CGI handling
import cgi 

base_url="test"
courses=[]
marks=[]

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

	possible = getFuturePossibleCourses(courses)
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
        print "</tbody>"
        print "</table>"
        print "</div>"

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
                <div class="container">
                <div class="jumbotron">
                    <h1>Clever Course</h1>
                </div>
                <nav class="navbar navbar-expand-md bg-dark navbar-dark">
			<form class="form-inline" id="search-form">
				<input class="form-control mr-sm-2 type="text" name="searched_for" placeholder="Enter a subject...">
				<select name="mark">
					<option value="HD">HD</option>
					<option value="D">D</option>
					<option value="C">C</option>
					<option value="P">P</option>
					<option value="FAIL">Fail</option>
				</select>
				<button class="btn btn-success" type="submit" value="Add">Search</button>
	"""
	print "<input type='hidden' name='prevCourses' value='" + (",").join(courses) + "'>"
	print "<input type='hidden' name='prevMarks' value='" + (",").join(marks) + "'>"
	print """
			</form>
		</nav>
                </div>
	"""


main()
