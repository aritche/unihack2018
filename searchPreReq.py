def checkOptions(course,courseList):
	for NCcheck in course:
			if "|" in NCcheck:
				subjects = NCcheck.split("|")
				for element in subjects:
					if element not in courseList:
						return False
			elif NCcheck not in courseList:
				return False
	return True

def searchPreReq(currentCourses):
	#matches is a list of the unit codes that are possibilities.
	#This list is filled as the code iterates
	matches = []
	#opens the file to read
	with open("db.txt","r") as file:
		#creates the object data which is the text file in a different format
		data = file.readlines()
		#Does a for loop based on each line of the data
		for line in data:
			#splits the line based on commas
			lines = line.split(",")
			unitCode = lines.pop(0)
			#unitName = lines.pop(0)
			lines.pop(0)
			lines.pop(0)
			#creates an empty array for the requirement courses
			newCourses = []
			for preReq in lines:
				#clears the white spaces
				preReq = preReq.rstrip()
				#adds the courses to the array new courses
				newCourses.append(preReq)
				if newCourses[0]=="":
					matches.append(unitCode)
				#Goes to the checkOptions code and cofirms matches
				elif checkOptions(newCourses,currentCourses) == True:
					matches.append(unitCode)
						
	if (len(matches)!=0):
		return list(set(matches)) 
	else:	
		return "No correlation"




		
CCList = ["PSYC2001","PSYC2081","PSYC1011","PSYC1001","PSYC1111"] 
print searchPreReq(CCList)

