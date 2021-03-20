import sys
import parsing
import interpreter
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " <filename>")
else:
    code = open(sys.argv[1]).read()
    instructions = parsing.parse(code)
    runner = interpreter.CButNot(instructions)
    while runner.step():
        pass
