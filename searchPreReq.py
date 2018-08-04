
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