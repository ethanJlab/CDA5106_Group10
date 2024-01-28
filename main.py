#!/usr/bin/python
import os
import getopt
import sys
from AssemblyRecord import AssemblyRecord

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
	print("Revision: 01")

def main():
	tracefile = "defaulttrace.dat"
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
	#TODO: The rest of the implementation starts here, 
	#the Scheduling Queue, 
	#the Fully functional units and register file (the output file)
	#The loop here is just a temporary placeholder on fetching stuff from the Dispatch Queue
	while not DispatchQueue.isEmpty():
		print (DispatchQueue.removefromlist().getlineofcode())

if __name__ == "__main__":
    main()
