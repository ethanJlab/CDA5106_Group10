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
	durationcounter = 0
	ReadInstructionsQ = AssemblyRecord()
	ROB = list() # list of instructions
	DispatchQ = list() # list of instructions in IF or ID state
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
		ROB.append(theInstruction.copy())
		counter += 1

	while ROB or DispatchQ: #do
		#TODO: The rest of the implementation starts here, 

		#the DispatchQ is a list of instruction objects in IF or ID state.
		if DispatchQ:
			dcounter = 0
			while dcounter < len(DispatchQ):
				schdInst = DispatchQ.pop(dcounter)
				if schdInst.getCurrentState().getexecutionstate() == "IF":
					schdInst.setCurrentState(2, cyclecounter, durationcounter) # assign ID state
					print ("DEBUG Pop DispatchQ: ", schdInst.gettag(),
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
					DispatchQ.insert(dcounter, schdInst.copy())
					dcounter += 1
				else:
					schdInst.setCurrentState(3, cyclecounter, durationcounter) # else assign IS state
					print ("DEBUG Pop DispatchQ IS state: ", schdInst.gettag(),
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
					issueQ.append(schdInst.copy()) # place modified instruction in IS state Queue					
	
				durationcounter += 1
		else:
			print ("DispatchQ is currently empty at cycle " + str(cyclecounter))
			print ("DEBUG listLength of DispatchQ = " + str(len(DispatchQ)) + " Cycle number = " + str(cyclecounter))


		lcounter = 0
		while dispatchbool:
			if ROB:
				schdInst = ROB.pop(0)
				schdInst.setCurrentState(1, cyclecounter, lcounter) #FIXME: I think duration lcounter! totally needs fixing.
				DispatchQ.append(schdInst.copy()) # place modified instruction in DispatchQ
				
				if lcounter == 7:
					dispatchbool = False
				else:
					dispatchbool = True
	
			else:
				print ("nothing to pop from ROB")
				print ("DEBUG listLength of DispatchQ = " + str(len(DispatchQ)) + " Cycle number = " + str(cyclecounter))
				print ("DEBUG listLength of issueQ = " + str(len(issueQ)) + " Cycle number = " + str(cyclecounter))
				break # once ROB is empty, this is the "while" part of the do .. while
			
			lcounter += 1
			durationcounter += 1

		dispatchbool = True #reset dispatchbool
		cyclecounter += 1 # advance the cycle.
		durationcounter += 1
		# END while ROB
		

if __name__ == "__main__":
    main()
