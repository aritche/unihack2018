class Course(object):
    unitName = ""
    preReq1 = ""
    preReq2 = ""

def makeNewCourse(unitName, preReq1 = "", preReq2 = ""):
	course = Course
	course.unitName = unitName
	course.preReq1 = preReq1
	course.preReq2 = preReq2
	return course
	

# **with open("db.txt","r") as file:
	# data = file.readlines()
	# for line in data:

		# lines = line.split(",")
		# print lines
		# for words in lines:
			# words = words.replace("\n", "")
		# length = len(words)
		# if(length == 1):
			# unit1 = makeNewCourse(words[0])
		# elif(length == 2):
			# unit2 = makeNewCourse(words[0],words[1])
		# elif(length == 3):
			# unit3 = makeNewCourse(words[0],words[1],words[2])

			
			
def searchPreReq(currentCourses):
	matches = []
	with open("db.txt","r") as file:
		data = file.readlines()
		for line in data:
			lines = line.split(", ")
			subject = lines.pop(0)
			#print line
			newCourses = []
			for preReq in lines:
				preReq = preReq.rstrip()
				newCourses.append(preReq)
				
				#print newCourses
				for courses in currentCourses:
					
					if courses in newCourses:
						matches.append(courses)
	return list(set(matches)) 
					
CCList = ["ACCT4444","BSBS2213"]
print searchPreReq(CCList)