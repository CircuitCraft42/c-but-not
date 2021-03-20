from parsimonious.grammar import Grammar
from parsimonious.exceptions import IncompleteParseError
grammar = Grammar(open("language.peg").read())
raw_code = open("test.txt", 'r').read() # modify this later to receive a filename from main program
preproc_out = ""
commented = False # currently inside a block comment
for line in raw_code.split('\n'):
    if commented:
        if "*/" in line:
            commented = False
            line = line[line.index("*/")+2:]
        else:
            continue
    if line.startswith("#"):
        continue # skip #define or whatever
    if "//" in line:
        preproc_out += line[:line.index("//")] + '\n'
    elif "/*" in line:
        preproc_out += line[:line.index("/*")] + '\n'
        commented = True
    else:
        preproc_out += line + '\n'
print(preproc_out)
try:
    tree = grammar.parse(preproc_out)
except IncompleteParseError:
    print("Syntax error somewhere!")
else:
    print(tree)
