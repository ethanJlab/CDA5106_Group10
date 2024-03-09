import sys
import copy
# IF: Instruction Fetch
# ID: Instruction Decode
# IS: Issue
# EX: Execute
# WB: Write Back
class state(object):
	def __init__(self, initstate, cyclep, durationp):
		self.executionstates = ["NA", "IF", "ID", "IS", "EX", "WB"]
		self.executionstate = self.executionstates[initstate]
		self.cycle = cyclep
		self.duration = durationp

	def copy(self):
		return copy.deepcopy(self)

	def getexecutionstate(self):
		return self.executionstate

	def setexecutionstate(self, thestate, thecycle, theduration):
		self.executionstate = self.executionstates[thestate]
		self.cycle = thecycle
		self.duration = self.duration + theduration

	def setcycle(self, thecycle):
		self.cycle = thecycle

	def getcycle(self):
		return self.cycle

	def setduration(self, theduration):
		self.duration = theduration

	def getduration(self):
		return self.duration

