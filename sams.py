from enum import Enum, auto

class State(Enum):
    IF = auto()  
    ID = auto()  
    IS = auto()  
    EX = auto() 
    WB = auto()  

class Instruction:
    OP_TYPE_MAPPING = {
        0: "ADD",
        1: "SUB",
        2: "MUL"
    }
    OP_TYPE_LATENCY = {
        0: 1,
        1: 1,
        2: 3 # fake it
    }
    def __init__(self, seq_num, op_type, src1, src2, dest):

        assert op_type in [0,1,2], "Invalid op_type"

        self.seq_num = seq_num
        self.op_type = op_type
        self.src1 = src1
        self.src2 = src2
        self.dest = dest
        self.state = State.IF
        self.execution_timer = self.OP_TYPE_LATENCY[op_type]

    def operands_are_ready(self, register):

        return register.is_register_ready(self.src1) and register.is_register_ready(self.src2)

class Register:
    def __init__(self):
        self.registers = {} 

    def set_register_ready(self, reg, ready=True):
        self.registers[reg] = ready

    def is_register_ready(self, reg):
        return self.registers.get(reg, True)  # Assume registers are ready by default

    def mark_registers_not_ready(self, instruction):
        self.set_register_ready(instruction.dest, False)

    def update_after_writeback(self, instruction):
        self.set_register_ready(instruction.dest, True)


class ROB:
    def __init__(self, filename, size=1024):
        self.size = size
        self.instructions = self.parse_trace_file(filename)
    
    def add_instruction(self, instruction):
        if len(self.instructions) < self.size:
            self.instructions.append(instruction)
        else:
            raise Exception("ROB overflow")
    
    def remove_instruction(self):
        if self.instructions:
            return self.instructions.pop(0)
        return None

    @staticmethod
    def parse_trace_file(file_path):
        instructions = []
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 5:
                    pc, op_type, dest, src1, src2 = parts
                    instruction = Instruction(pc, int(op_type), int(src1), int(src2), int(dest))
                    instructions.append(instruction)
        return instructions

class Simulator:

    def __init__(self, filename, issue_queue_size=10):
        self.dispatch_list = []
        self.issue_list = []
        self.execute_list = []
        self.rob = ROB(filename)
        self.issue_queue_size = issue_queue_size
        self.register = Register()

    def fake_retire(self):
        while self.rob.instructions and self.rob.instructions[0].state == State.WB:
            instruction = self.rob.remove_instruction()
            self.register.update_after_writeback(instruction)

    def execute(self):
        for instruction in self.execute_list[:]:
            if instruction.execution_timer > 0:
                instruction.execution_timer -= 1
                if instruction.execution_timer == 0:
                    instruction.state = State.WB
                    self.execute_list.remove(instruction)
                    # TODO:  3) Update the register file state e.g., ready flag) and wakeup
                    #           dependent instructions (set their operand ready flags)

    def issue(self):
        ready_instructions = [instr for instr in self.issue_list if instr.operands_are_ready(self.register)]
        for instruction in sorted(ready_instructions, key=lambda x: x.seq_num)[:self.issue_queue_size]: # N+1
            self.issue_list.remove(instruction)
            self.execute_list.append(instruction)
            instruction.state = State.EX
            self.register.mark_registers_not_ready(instruction)

    def dispatch(self):
        id_instructions = [instr for instr in self.dispatch_list if instr.state == State.ID]
        for instruction in sorted(id_instructions, key=lambda x: x.seq_num):

            self.dispatch_list.remove(instruction)
            self.issue_list.append(instruction)
            instruction.state = State.IS
            # TODO: Increment issue queue count, decrement dispatch queue count

if __name__ == '__main__':

    simulator = Simulator("tracefile.dat")
    while simulator.rob.instructions or simulator.dispatch_list:
        simulator.fake_retire()
        simulator.execute()
        simulator.issue()
        simulator.dispatch()
