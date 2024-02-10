#!/usr/bin/python
import os
import getopt
import sys
from AssemblyRecord import AssemblyRecord
from instruction import instruction


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
	print("Revision: 02")

def main():
	tracefile = "defaulttrace.dat"
	counter = 0
	schedulingQ = list()

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
	DispatchQueue = AssemblyRecord()
	DispatchQueue.readAssemblyFile(tracefile)
	
	while not DispatchQueue.isEmpty():
		result_token = DispatchQueue.removefromlist().getlineofcode().split()
		theInstruction = instruction(result_token[0], result_token[1], result_token[2], result_token[3], result_token[4], str(counter))
		schedulingQ.append(theInstruction.copy())
		counter += 1
	
	FunctionUnitQ = list()

	while schedulingQ:
		#TODO: The rest of the implementation starts here, 
		#starting with the scheduling queue which holds a list of instruction objects which include the tags, 
		#the Fully functional units, Register Objects, and outputfile
		#The loop here is just a temporary placeholder on fetching stuff from the schedulingQ, 
		#the schedulingQ is a list of instruction objects
		schdInst = schedulingQ.pop(0)
		print ("DEBUG The Schd instruction: ", schdInst.gettag(),
				schdInst.getpc(), 
				schdInst.getopt(), 
				schdInst.getdst(), 
				schdInst.getsrc1(), 
				schdInst.getsrc2())

if __name__ == "__main__":
    main()
