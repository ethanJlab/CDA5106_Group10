import sys
from CustomDataRecord import CustomDataRecord
class AssemblyRecord:
	def __init__(self):
		self.AssemblyRecordList = list()

	def __call__(self):
		self.AssemblyRecordList = list()

	def addtolist(self, item2add):
		self.AssemblyRecordList.append(item2add)

	def removefromlist(self):
		if not self.AssemblyRecordList:
			return [0]
		else:
			return self.AssemblyRecordList.pop(0)

	def popfromlist(self):
		if not self.AssemblyRecordList:
			return [0]
		else:
			return self.AssemblyRecordList.pop()

	def isEmpty(self):
		if not self.AssemblyRecordList:
			return True
		else:
			return False

	def clearlist(self):
		del self.AssemblyRecordList[:]

	def readAssemblyFile(self, filename):
		cd2 = CustomDataRecord()
		try:
			fileptr = open(str(filename), 'r')
			while True:
				try:
					isIgnoreLine = cd2.LoadStreamFile(fileptr)
					if isIgnoreLine == False:
						self.addtolist(cd2.copy())
					else:
						print ("ignore line...")
				except EOFError:
					print ("End of File, leaving...")
					fileptr.close()
					break
		except IOError:
			print ("IOError: No such file!")

