import sys, os
import parsing
import interpreter
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " <filename>")
else:
    retcode = os.system("cc " + sys.argv[1] + " -o /dev/null > /dev/null 2> /dev/null")
    if retcode:
        print("ERROR: Program is not valid C.")
    else:
        code = open(sys.argv[1]).read()
        instructions = parsing.parse(code)
        runner = interpreter.CButNot(instructions)
        runner.run()
