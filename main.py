#!/usr/bin/python
import os
import getopt
import sys
from AssemblyRecord import AssemblyRecord
from instruction import instruction
from RegisterClass import Register


def show_help_screen():
	print("Options:")
	print("  -h, --help .................................... This help screen")
	print("  -v, --version ................................. Display Version")
	print("  -f, --file=<filename> ......................... Input trace file")
	print("Examples executions:")
	print("python main.py --file=tracefile.dat")
	print("python main.py --f=tracefile.dat")
	print("python main.py -f tracefile.dat")
	print("python main.py -ftracefile.dat")
	print('')

def show_version():
	print("Version: 00")
	print("Revision: 03")

def main():
	tracefile = "defaulttrace.dat"
	counter = 0
	cyclecounter = 0
	ReadInstructionsQ = AssemblyRecord()
	DispatchQ = list() # list of instructions in IF or ID state
	InstructionsIF = list() # list of instructions in IF state
	issueQ = list() # list of instructions in IS state (issue state)
	executeQ = list() # list of instructions in EX state (execute state)
	registers = Register()
	dispatchbool = True

	try:
		opts, args = getopt.getopt(sys.argv[1:],"h*:v*:f:",["help", "version", "file="])
	except getopt.GetoptError:
		print("GET OPT ERROR, printing help screen")
		show_help_screen()
		sys.exit(1)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			show_help_screen()
			sys.exit(1)
		elif opt in ("-v", "--version"):
			show_version()
			sys.exit(1)
		elif opt in ("-f", "--file"):
			tracefile = arg

	print("tracefile:", tracefile)
	ReadInstructionsQ.readAssemblyFile(tracefile)
	
	while not ReadInstructionsQ.isEmpty():
		result_token = ReadInstructionsQ.removefromlist().getlineofcode().split()
		theInstruction = instruction(result_token[0], result_token[1], result_token[2], result_token[3], result_token[4], str(counter))
		DispatchQ.append(theInstruction.copy())
		counter += 1

	while DispatchQ: #TODO: This while loop needs to be a bit smarter...
		#TODO: The rest of the implementation starts here, 

		#the DispatchQ is a list of instruction objects in IF or ID state.
		lcounter = 0
		while dispatchbool:
			schdInst = DispatchQ.pop(lcounter)
			schdInst.setIFstate(0, cyclecounter, lcounter) #FIXME: I think duration lcounter! totally needs fixing.
			
			DispatchQ.insert(lcounter, schdInst.copy()) #place modified instruction back in DispatchQ
			if lcounter == 7:
				dispatchbool = False
			else:
				dispatchbool = True

			lcounter += 1
		
		#TODO: DEBUG code only
		schdInst = DispatchQ.pop(0)
		print ("DEBUG The modifed Schd instruction: ", schdInst.gettag(),
				schdInst.getpc(), 
				schdInst.getopt(), 
				schdInst.getdst(), 
				schdInst.getsrc1(), 
				schdInst.getsrc2(), 
				schdInst.getIFstate().getexecutionstate(), 
				schdInst.getIFstate().getcycle(),
				schdInst.getIFstate().getduration(), 
				schdInst.getIDstate().getexecutionstate(), 
				schdInst.getIDstate().getcycle(),
				schdInst.getIDstate().getduration(),
				schdInst.getISstate().getexecutionstate(), 
				schdInst.getISstate().getcycle(),
				schdInst.getISstate().getduration(),
				schdInst.getEXstate().getexecutionstate(), 
				schdInst.getEXstate().getcycle(),
				schdInst.getEXstate().getduration(),
				schdInst.getWBstate().getexecutionstate(), 
				schdInst.getWBstate().getcycle(),
				schdInst.getWBstate().getduration())

		cyclecounter += 1 # advance the cycle.
		

if __name__ == "__main__":
    main()
