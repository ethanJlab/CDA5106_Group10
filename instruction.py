import sys
import copy
from state import state
class instruction(object):
	def __init__(self, pc, opt, dst, src1, src2, tag):
		self.pc = pc
		self.opt = opt
		self.dst = dst
		self.src1 = src1
		self.src2 = src2
		self.tag = tag
		self.executionstate = state(0)

	def copy(self):
		return copy.deepcopy(self)

	def getpc(self):
		return self.pc

	def getopt(self):
		return self.opt

	def getdst(self):
		return self.dst

	def getsrc1(self):
		return self.src1

	def getsrc2(self):
		return self.src2

	def gettag(self):
		return self.tag

	def setexecutionstate(self, value):
		self.executionstate.setexecutionstate(value)

	def getexecutionstate(self):
		return self.executionstate 
