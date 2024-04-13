import sys

class State:
    IF = 'IF'
    ID = "ID"
    IS = "IS"
    EX = "EX"
    WB = "WB"

class Instruction:
    OP_TYPE_LATENCY = {
        0: 1,
        1: 2,
        2: 5 
    }
    def __init__(self, pc, op_type, src1, src2, dest, tag):

        assert op_type in [0,1,2], "Invalid op_type"

        self.pc = pc
        self.op_type = op_type
        self.src1 = src1
        self.src2 = src2
        self.dest = dest

        self.orig_src1 = src1
        self.orig_src2 = src2

        self.state = State.IF
        self.latency = self.OP_TYPE_LATENCY[op_type]
        self.tag = tag

        self.IF = self.ID = self.IS = self.EX = self.WB = (None, 1) # (cycle, duration)

    def operands_are_ready(self):

        return self.src1 == -1 and self.src2 == -1
        
    def __repr__(self) -> str:
        return f"Inst(tag[{self.tag}] op[{self.op_type}] s1[{self.src1}] s2[{self.src2}] d[{self.dest}] lat[{self.latency}] st[{self.state}] IF[{self.IF}] ID[{self.ID}] IS[{self.IS}] EX[{self.EX}] WB[{self.WB}]"


class Simulator:

    def __init__(self, scheduling_queue_size=2, fetch_size=8, filename="val_trace_gcc.dat"):
        
        scheduling_queue_size = int(scheduling_queue_size)
        fetch_size = int(fetch_size)

        self.dispatch_list = [] # 2 * issue_queue_size
        self.issue_list = []
        self.filename = filename
        self.execute_list = []
        self.rob = []
        self.scheduling_queue_size = scheduling_queue_size # reservation station size
        self.dispatch_queue_size = 2 * fetch_size
        self.fetch_size = fetch_size
        self.register = [-1] * 128 # -1 indicates register is ready
        self.cycle_counter = 0
        self.instruction_counter = 0
        self.fu = [-1] * (fetch_size + 1) # functional units, -1 indicates free

        self.instruction_generator = self.read_next_instruction()
        self.is_end_of_trace_file = False

    def fake_retire(self):
        while self.rob and self.rob[0].state == State.WB:
            instruction = self.rob.pop(0)
            # since we are faking the rob, we don't need to update 
            # the register state when instruction is retired from ROB
            # self.register[instruction.dest] = -1
            print(f"{instruction.tag} " +
                  f"fu{{{instruction.op_type}}} src{{{instruction.orig_src1},{instruction.orig_src2}}} dst{{{instruction.dest}}} " +
                  f"IF{{{instruction.IF[0]},{instruction.IF[1]}}} ID{{{instruction.ID[0]},{instruction.ID[1]}}} IS{{{instruction.IS[0]},{instruction.IS[1]}}} " +
                  f"EX{{{instruction.EX[0]},{instruction.EX[1]}}} WB{{{instruction.WB[0]},{instruction.WB[1]}}}")

    def execute(self):
        unfinished_instructions = []
        for instruction in self.execute_list:

            instruction.latency -= 1

            if instruction.latency == 0:
                instruction.state = State.WB
                instruction.WB = (self.cycle_counter, 1)

                # it's possible that the renamed tag is overwritten by another instruction
                # so check if this instruction is the latest one to write to the register
                if self.register[instruction.dest] == instruction.tag:
                    self.register[instruction.dest] = -1
                
                # broadcast source operand ready in the issue list
                for instr in self.issue_list:
                    if instr.src1 == instruction.tag:
                        instr.src1 = -1
                    if instr.src2 == instruction.tag:
                        instr.src2 = -1
            else:
                instruction.EX = (instruction.EX[0], instruction.EX[1] + 1)
                unfinished_instructions.append(instruction)
        
        self.execute_list = unfinished_instructions

    def fetch(self):
        n_fetched = 0

        while n_fetched < self.fetch_size and len(self.dispatch_list) < self.dispatch_queue_size:
            try:
                instruction = next(self.instruction_generator)
                instruction.IF = (self.cycle_counter, 1)
                self.rob.append(instruction)
                self.dispatch_list.append(instruction)
                n_fetched += 1
            except StopIteration:
                self.is_end_of_trace_file = True
                break

    def issue(self):
        ready_instructions = []
        stall_instructions = []

        for instr in self.issue_list:
            if instr.operands_are_ready() and len(ready_instructions) < self.fetch_size + 1:
                ready_instructions.append(instr)
            else:
                instr.IS = (instr.IS[0], instr.IS[1] + 1)
                stall_instructions.append(instr)

        for instruction in sorted(ready_instructions, key=lambda x: x.tag): # N+1
            self.execute_list.append(instruction)
            instruction.state = State.EX
            instruction.EX = (self.cycle_counter, 1)
        
        self.issue_list = stall_instructions

    def dispatch(self): 

        id_instructions = []
        if_instructions = []
        for instruction in self.dispatch_list:
            if instruction.state == State.ID:
                id_instructions.append(instruction)
            else:
                if_instructions.append(instruction)

        id_instructions = sorted(id_instructions, key=lambda x: x.tag)

        while id_instructions and len(self.issue_list) < self.scheduling_queue_size:
            instruction = id_instructions.pop(0)
            self.issue_list.append(instruction)
            instruction.state = State.IS
            instruction.IS = (self.cycle_counter, 1)
            # renaming
            if instruction.src1 != -1:
                instruction.src1 = self.register[instruction.src1]
            if instruction.src2 != -1:
                instruction.src2 = self.register[instruction.src2]
            if instruction.dest != -1:
                self.register[instruction.dest] = instruction.tag  
            
        self.dispatch_list = id_instructions + if_instructions
        for instr in self.dispatch_list:
            instr.state = State.ID
            if instr.ID[0] == None:
                instr.ID = (self.cycle_counter, 1)
            else:
                instr.ID = (instr.ID[0], instr.ID[1] + 1)

    def read_next_instruction(self):

        with open(self.filename, 'r') as file:
            for line in file:
                line = line.rstrip()
                pc, op_type, dest, src1, src2 = line.strip().split()
                instruction = Instruction(pc, int(op_type), int(src1), int(src2), int(dest), self.instruction_counter)
                self.instruction_counter += 1
                yield instruction

    def run(self):
        while self.rob or self.dispatch_list or  self.issue_list or not self.is_end_of_trace_file:
            self.fake_retire()
            self.execute()
            self.issue()
            self.dispatch()
            self.fetch()
            self.cycle_counter += 1

        self.cycle_counter -= 1
        print(f"number of instructions = {self.instruction_counter}")
        print(f"number of cycles       = {self.cycle_counter}")
        print(f"IPC                    = {self.instruction_counter / self.cycle_counter:.5f}")

if __name__ == '__main__':

    simulator = Simulator(*sys.argv[1:])
    simulator.run()
