import sys
import copy
class CustomDataRecord(object):
	def __init__(self):
		self.lineofcode = str("")

	def copy(self):
		return copy.deepcopy(self)

	def getlineofcode(self):
		return self.lineofcode

	def LoadStreamFile(self, Input):
		try:
			rawline = Input.readline()
			if not rawline:
				print('end of line')
				raise EOFError

			if rawline[0] != '#':
				self.lineofcode = rawline
				return False #VALID LINE
			else:
				return True #Comment Line

		except EOFError:
			print ("End of File, rasing EOF")
			raise EOFError
		except IndexError:
			return True #escape out

