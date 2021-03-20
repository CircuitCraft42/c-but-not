import re

_word_delimiter = re.compile(r'[^a-z]')

def combine_results(results):
    if len(results) == 0:
        return True
    if len(results) == 1:
        return results[0] != 0
    if len(results) == 2:
        return bool(results[0] and results[1])
    if len(results) == 3:
        return bool(results[int(bool(results[0]))+1])

_registers = ['+', '-', '*', '/', '%', '&', '|', '^', '<<', '>>']
class CButNot:
    def __init__(self, commands, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = commands
        self.command_idx = commands.index("main")
        self.registers = {}
        self.stack = []
        self.buffer = {}
        self.current_register = -1
        self.cmds = {}
        for member in dir(self):
            if member.startswith('cmd_'):
                self.cmds[member[4:]] = getattr(self, member)
    def shift_register(self, offset):
        reg = self.current_register + offset
        self.current_register = reg % len(_registers)
    def get_register(self):
        return self.registers.get(_registers[self.current_register], 0)
    def set_register(self, value):
        self.registers[_registers[self.current_register]] = value

    def step(self):
        idx = self.command_idx + 1
        cmd = self.commands[idx]
        while isinstance(cmd, str): idx += 1
        if isinstance(cmd, tuple):
            self.execute_command(*cmd)
        elif isinstance(cmd, list) and self.check_jump(cmd[1]):
            idx = self.commands.index[cmd[0]]
        self.command_idx = idx

    def execute_command(self, prefix, register, postfix):
        self.current_register = _registers.index(register)
        value = self.registers.get(register, 0)
        value = self.execute_fragment(prefix, 'prefix', value)
        value = self.execute_fragment(postfix, 'postfix', value)
        self.registers[register] = value
        return value
    def execute_fragment(self, fragment, position, value):
        while True:
            while fragment and not fragment[:1].isalpha():
                fragment = fragment[1:]
            if not fragment:
                break
            delimiter_match = _word_delimiter.search(fragment, 1)
            delimiter_pos = delimiter_match.start() if delimiter_match is not None else len(fragment)
            cmd = fragment[:delimiter_pos]
            fragment = fragment[delimiter_pos:]
            value = self.execute_cmd(cmd.lower(), position, value)
        return value
    def execute_cmd(self, cmd, position, value):
        return self.cmds[cmd](position, value)
    def check_jump(self, operations):
        results = list(map(lambda op: execute_command(*op)))
        return combine_results(results)

    def cmd_idx(self, position, value):
        added_value = self.stack.pop() if position == 'prefix' else 1
        return value + added_value
    def cmd_ptr(self, position, value):
        if position == 'prefix':
            return self.stack.pop()
        else:
            self.stack.append(value)
            return value
    def cmd_tbl(self, position, value):
        if position == 'prefix':
            self.stack.append(value)
            return self.buffer.get(value, 0)
        else:
            address = self.stack.pop()
            self.buffer[address] = value
            return address
    def cmd_cnt(self, position, value):
        subtracted_value = self.stack.pop() if position == 'prefix' else 1
        return value - subtracted_value
    def cmd_x(self, position, value):
        if position == 'prefix':
            self.stack.append(value)
            self.shift_register(1)
            return self.get_register()
        else:
            self.set_register(value)
            self.shift_register(-1)
            return self.stack.pop()
    def cmd_y(self, position, value):
        if position == 'prefix':
            self.stack.append(value)
            self.shift_register(-1)
            return self.get_register()
        else:
            self.set_register(value)
            self.shift_register(1)
            return self.stack.pop()
    def cmd_index(self, position, value):
        if position == 'prefix':
            self.stack.append(0)
        else:
            del self.stack[-1]
        return value
    def cmd_i(self, position, value):
        return value
    def cmd_pointer(self, position, value):
        self.stack.append(self.stack[-1])
        return value
    def cmd_table(self, position, value):
        if position == 'prefix':
            self.stack.append(self.stack.pop(-value))
        else:
            self.stack.insert(-value, self.stack.pop())
        return value