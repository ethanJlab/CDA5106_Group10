import sys
import copy
# IF: Instruction Fetch
# ID: Instruction Decode
# IS: Issue
# EX: Execute
# WB: Write Back
class state(object):
	def __init__(self, initstate):
		self.executionstates = ["IF", "ID", "IS", "EX", "WB"]
		self.executionstate = self.executionstates[0]

	def copy(self):
		return copy.deepcopy(self)

	def getexecutionstate(self):
		return self.executionstate

	def setexecutionstate(self, thestate):
		self.executionstate = self.executionstates[thestate]

