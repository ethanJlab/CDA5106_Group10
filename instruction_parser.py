

op_cycle_mapping = {0: 1, 1: 2, 2: 5}

def parse_instructions(instructions):
    """
    Args:
    - instructions (list of str): Instructions in the format '<PC> <operation type> <dest reg #> <src1 reg #> <src2 reg #>'

    Returns:
    - List of lists, where each sublist contains instructions that can be executed in parallel.
    """
    parsed_instructions = []
    for instr in instructions:
        parts = instr.split()
        parsed_instructions.append({
            'PC': parts[0],
            'op_type': int(parts[1]),
            'dest_reg': int(parts[2]),
            'src1_reg': int(parts[3]),
            'src2_reg': int(parts[4]),
        })

    dependencies = {i: [] for i in range(len(parsed_instructions))}
    last_write = {}
    reads = {}

    for i, instr in enumerate(parsed_instructions):
        src_regs = [r for r in [instr['src1_reg'], instr['src2_reg']] if r != -1]
        dest_reg = instr['dest_reg']

        # RAW dep
        for reg in src_regs:
            if reg in last_write:
                dependencies[last_write[reg]].append(i)
            if reg in reads:
                for reader in reads[reg]:
                    dependencies[reader].append(i)

        # WAR and WAW dep
        if dest_reg != -1:
            if dest_reg in reads:
                for reader in reads[dest_reg]:
                    dependencies[reader].append(i)
                del reads[dest_reg]  # Clear after dependency resolution
            if dest_reg in last_write:
                dependencies[last_write[dest_reg]].append(i)
            last_write[dest_reg] = i
            reads[dest_reg] = [i] if dest_reg not in reads else reads[dest_reg] + [i]

    executed = set()
    chunks = []
    process_id = 0
    while len(executed) < len(parsed_instructions):
        chunk = [f"Process {process_id}"]
        for i in range(len(parsed_instructions)):
            if i in executed:
                continue

            if all(dep in executed for dep in dependencies[i]):
                chunk.append(instructions[i])
                executed.add(i)
        chunks.append(chunk)
        process_id += 1

    return chunks

if __name__ == '__main__':
    file_path = 'tracefile.dat'
    with open(file_path, 'r') as file:
        instructions = [line.strip() for line in file if line.strip()]
    chunks = parse_instructions(instructions)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk}")