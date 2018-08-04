def main():
	nLoops = input("How many subjects do you want to add? ")
	array = []
	for x in range(nLoops):
		subject = newCourseAndGrade(raw_input("Enter the course id:"),raw_input("Enter your mark in the form of HD, D, C, or P: "))
		array.append(subject)
	array.sort(key=lambda x: x.mark, reverse = True) # sort by mark
	for elements in array:
		print elements.unitCode
		getRecords(elements.unitCode)

class courseAndGrade(object):
	unitCode = ""
	mark = 0

def newCourseAndGrade(unitCode, grade):
	course = courseAndGrade()
	course.unitCode = unitCode
	if grade == "HD":
		course.mark = 1
	elif grade == "D":
		course.mark = 0.7
	elif grade == "C":
		course.mark = 0.4
	elif grade == "P":
		course.mark = 0.1
	else:
		course.mark = 0
	return course
	
def getRecords(course):
	#SORT UNITS BASED ON GRADE	
	possible = getFuturePossibleCourses(course)
	for item in possible[0]:
		print "<p>" + item + "</p>"
	#for item in possible[1]:
	#	print "<p style=\"color:red\">" + item + "<br>"

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
		
		
main()