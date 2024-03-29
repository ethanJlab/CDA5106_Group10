class Register:
    def __init__(self):
        # Initialize 128 registers, all set to zero initially
        self.registers = [0 for _ in range(128)]

    def set_value(self, reg_num, value):
        # Set the value of a register
        if 0 <= reg_num < 128:
            self.registers[reg_num] = value
        elif reg_num == -1:
            # -1 indicates no operation on this register
            pass
        else:
            raise ValueError("Register number out of range")

    def get_value(self, reg_num):
        # Get the value of a register
        if 0 <= reg_num < 128:
            return self.registers[reg_num]
        elif reg_num == -1:
            # -1 indicates no operation on this register
            return None
        else:
            raise ValueError("Register number out of range")

    def reset_registers(self):
        # Reset all registers to zero
        self.registers = [0 for _ in range(128)]
