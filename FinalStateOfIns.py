import sys
from instruction import instruction
class FinalStateOfIns:
	def __init__(self):
		self.instructionlist = list()

	def __call__(self):
		self.instructionlist = list()

	def addtolist(self, item2add):
		self.instructionlist.append(item2add)

	def removefromlist(self):
		if not self.instructionlist:
			return [0]
		else:
			return self.instructionlist.pop(0)

	def popfromlist(self):
		if not self.instructionlist:
			return [0]
		else:
			return self.instructionlist.pop()

	def isEmpty(self):
		if not self.instructionlist:
			return True
		else:
			return False

	def clearlist(self):
		del self.instructionlist[:]

	def WriteToFile(self, filename):
		fileptr = open(filename, 'w')

		while not self.isEmpty():
			cd = self.removefromlist()
			cd.WriteToFile(fileptr)

		fileptr.close()

