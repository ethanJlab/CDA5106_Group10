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
		self.CurrentState = state(0, 0, 0)
		self.IFstate = state(0, 0, 0)
		self.IDstate = state(0, 0, 0)
		self.ISstate = state(0, 0, 0)
		self.EXstate = state(0, 0, 0)
		self.WBstate = state(0, 0, 0)
		self.operandFlag = False # True if operands are ready, False if operands are not ready

	def setoperandFlag(self, value):
		self.operandFlag = value

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

	def setCurrentState(self, value, cycle, duration):
		self.CurrentState.setexecutionstate(value, cycle, duration)
		if value == 1:
			self.__setIFstate(value, cycle, duration)
		elif value == 2:
			self.__setIDstate(value, cycle, duration)
		elif value == 3:
			self.__setISstate(value, cycle, duration)
		elif value == 4:
			self.__setEXstate(value, cycle, duration)
		elif value == 5:
			self.__setWBstate(value, cycle, duration)

	def getCurrentState(self):
		return self.CurrentState

	def getIFstate(self):
		return self.IFstate 

	def getIDstate(self):
		return self.IDstate 

	def getISstate(self):
		return self.ISstate 

	def getEXstate(self):
		return self.EXstate 

	def getWBstate(self):
		return self.WBstate

	def WriteToFile(self, Output):
		spacestr = " "
		commastr = ","
		writestr = (self.tag + spacestr + "fu{" + self.opt + "}" + 
					spacestr + "src{" + self.src1 + commastr + self.src2 + "}" + spacestr + 
					"dst{" + self.dst + "}" + spacestr + 
					"IF{" + str(self.IFstate.getcycle()) + commastr + str(self.IFstate.getduration()) + "}" + spacestr +
					"ID{" + str(self.IDstate.getcycle()) + commastr + str(self.IDstate.getduration()) + "}" + spacestr +
					"IS{" + str(self.ISstate.getcycle()) + commastr + str(self.ISstate.getduration()) + "}" + spacestr +
					"EX{" + str(self.EXstate.getcycle()) + commastr + str(self.EXstate.getduration()) + "}" + spacestr +
					"WB{" + str(self.WBstate.getcycle()) + commastr + str(self.WBstate.getduration()) + "}" + spacestr)
		writestr = writestr + "\n"
		Output.write(writestr)

	# private members:

	def __setIFstate(self, value, cycle, duration):
		self.IFstate.setexecutionstate(value, cycle, duration)

	def __setIDstate(self, value, cycle, duration):
		self.IDstate.setexecutionstate(value, cycle, duration)

	def __setISstate(self, value, cycle, duration):
		self.ISstate.setexecutionstate(value, cycle, duration)

	def __setEXstate(self, value, cycle, duration):
		self.EXstate.setexecutionstate(value, cycle, duration)

	def __setWBstate(self, value, cycle, duration):
		self.WBstate.setexecutionstate(value, cycle, duration)

