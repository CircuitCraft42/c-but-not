from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from parsimonious.exceptions import IncompleteParseError
class CBNVisitor(NodeVisitor):
    def generic_visit(self, node, visited_children):
        """ Returns node or nested array of them. """
        return visited_children or node

    def visit_identifier(self, node, visited_children):
        """ Returns the text of the identifier. """
        return node.text

    def visit_operator(self, node, visited_children):
        """ Returns the operator. """
        return node.text

    def visit_ws(self, node, visited_children):
        return ""

    def visit_exprstmt(self, node, visited_children):
        """ Returns the instruction triples. """
        instructions = []
        last = visited_children[0]
        cur = visited_children[2]
        for v in cur:
            instructions.append((last, v[0], v[2]))
            last = v[2]
        return instructions

    def visit_decl(self, node, visited_children):
        return []

    def visit_function(self, node, visited_children):
        fxname = visited_children[2]
        instructions = [fxname]
        for stmt in visited_children[-3]:
            instructions += stmt[0]
        return instructions

    def visit_program(self, node, visited_children):
        instructions = []
        for child in visited_children[-1]:
            instructions += child[0]
        return instructions
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
try:
    tree = grammar.parse(preproc_out)
except IncompleteParseError:
    print("Syntax error somewhere!")
else:
    instructions = CBNVisitor().visit(tree)
    print(instructions)
