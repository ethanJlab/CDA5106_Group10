#!/usr/bin/python
import os
import getopt
import sys
from AssemblyRecord import AssemblyRecord
from instruction import instruction
from RegisterClass import Register
from FinalStateOfIns import FinalStateOfIns


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
	print("Version: 01")
	print("Revision: 00")

# General function to print the state of the instruction
def print_schdInst(message, schdInst):
    print(message,
          schdInst.gettag(),
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

def main():
	tracefile = "defaulttrace.dat"
	counter = 0
	cyclecounter = 0
	durationcounter = 0

	#TODO: maxScheduleQSize and maxDispatch should be read as input
	maxScheduleQSize = 2
	maxDispatch = 8
	
	ReadInstructionsQ = AssemblyRecord()
	FinalStateOfInstructions = FinalStateOfIns()
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

	while ROB or DispatchQ or issueQ or executeQ: #do
		durationcounter = 0
		# From the execute_list, check for instructions that are finishing
		while executeQ: 
			schdInst = executeQ.pop(0)
			print_schdInst("Debug Pop executeQ: ", schdInst)
			schdInst.setCurrentState(5, cyclecounter, durationcounter)
			# TODO: Update the register file state (ready flag) and wakeup
			# TODO: set the operand ready flag of dependent instructions
			FinalStateOfInstructions.addtolist(schdInst.copy())
			durationcounter += 1
			#cyclecounter += 1
		# Scan the READY instructions and issue up to N+1 of them						
		while issueQ and len(executeQ) < maxScheduleQSize + 1:
			# TODO: only opperands that are "ready" should be added here
			schdInst = issueQ.pop(0)
			print_schdInst("DEBUG Pop issueQ: ", schdInst)
			schdInst.setCurrentState(4, cyclecounter, durationcounter)
			durationcounter += 1
			executeQ.append(schdInst.copy()) #place in execute Q
		#cyclecounter += 1

		#the DispatchQ is a list of instruction objects in IF or ID state.
		if DispatchQ:
			dcounter = 0
			while dcounter < len(DispatchQ) and len(issueQ) <= maxScheduleQSize:
				# TODO: fix, dont include instructions in the IF state to the list
				schdInst = DispatchQ.pop(dcounter)
				if schdInst.getCurrentState().getexecutionstate() == "IF":
					schdInst.setCurrentState(2, cyclecounter, durationcounter) # assign ID state
					print_schdInst("DEBUG Pop DispatchQ: ", schdInst)
					DispatchQ.insert(dcounter, schdInst.copy()) # and place it back
					dcounter += 1
				else:
					schdInst.setCurrentState(3, cyclecounter, durationcounter) # else assign IS state
					print_schdInst("DEBUG Pop DispatchQ IS state: ", schdInst)
					issueQ.append(schdInst.copy()) # place modified instruction in IS state Queue
					# TODO:	Rename source operands by looking up state in the register file
					# and rename destination by updating state in the register file
	
				durationcounter += 1 # increment duration again, because we are still doing stuff
				
		else:
			print ("DispatchQ is currently empty at cycle " + str(cyclecounter))
			print ("DEBUG listLength of DispatchQ = " + str(len(DispatchQ)) + " Cycle number = " + str(cyclecounter))


		lcounter = 0
		while dispatchbool:
			if ROB:
				schdInst = ROB.pop(0)
				schdInst.setCurrentState(1, cyclecounter, lcounter) # set to the IF state
				DispatchQ.append(schdInst.copy()) # place modified instruction in DispatchQ

				# The operation type of an instruction indicates its execution latency
				if schdInst.getopt() == "0": # Type 0 has a latency of 1 cycle
					lcounter += 1
				elif schdInst.getopt() == "1": # Type 1 has a latency of 2 cycles
					lcounter += 2
				elif schdInst.getopt() == "2": # Type 2 has a latency of 5 cycles
					lcounter += 5
				
				# the maximum amount of instructions that can be dispatched in one cycle is n + 1
				# Max length of DispatchQ is 2n			
				if lcounter >= maxDispatch or len(DispatchQ) >= 2*maxDispatch:
					dispatchbool = False
					cyclecounter += 1
				else:
					dispatchbool = True
	
			else:
				print ("nothing to pop from ROB")
				print ("DEBUG listLength of DispatchQ = " + str(len(DispatchQ)) + " Cycle number = " + str(cyclecounter))
				print ("DEBUG listLength of issueQ = " + str(len(issueQ)) + " Cycle number = " + str(cyclecounter))
				break # once ROB is empty, this is the "while" part of the do .. while
			
			#cyclecounter += 1
			lcounter += 1
			durationcounter += 1 # duration should be here as well as in the outside loop, because we are measuring 
									# how long we are here executing.

		dispatchbool = True #reset dispatchbool
		cyclecounter += 1 # advance the cycle.
		# END while ROB

	FinalStateOfInstructions.WriteToFile("output.txt")		

if __name__ == "__main__":
    main()
