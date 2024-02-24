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
		self.IFstate = state(0, 0, 0)
		self.IDstate = state(1, 0, 0)
		self.ISstate = state(2, 0, 0)
		self.EXstate = state(3, 0, 0)
		self.WBstate = state(4, 0, 0)

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

	def setIFstate(self, value, cycle, duration):
		self.IFstate.setexecutionstate(value, cycle, duration)

	def getIFstate(self):
		return self.IFstate 

	def setIDstate(self, value, cycle, duration):
		self.IDstate.setexecutionstate(value, cycle, duration)

	def getIDstate(self):
		return self.IDstate 

	def setISstate(self, value, cycle, duration):
		self.ISstate.setexecutionstate(value, cycle, duration)

	def getISstate(self):
		return self.ISstate 

	def setEXstate(self, value, cycle, duration):
		self.EXstate.setexecutionstate(value, cycle, duration)

	def getEXstate(self):
		return self.EXstate 

	def setWBstate(self, value, cycle, duration):
		self.WBstate.setexecutionstate(value, cycle, duration)

	def getWBstate(self):
		return self.WBstate 

