import functools
import itertools
import parsing
import re
import sys

split_ops_pattern = re.compile('[^a-z]')
def split_ops(ops):
    if not isinstance(ops, str):
        yield ops
    else:
        while ops:
            while split_ops_pattern.match(ops.lower()):
                ops = ops[1:]
            start_op = split_ops_pattern.search(ops, 1)
            slice_pos = start_op.start() if start_op else len(ops)
            op = ops[:slice_pos].lower()
            ops = ops[slice_pos:]
            yield op

code = sys.stdin.read()
ast = parsing.parse(code)

registers = ['+', '-', '*', '/', '%', '&', '|', '^', '<<', '>>']

header = """
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

intptr_t value;

#define NUM_REGISTERS {num_registers}
intptr_t registers[NUM_REGISTERS];
size_t cur_register;

intptr_t *stack = NULL;
size_t stack_cap = 0;
size_t stack_top = 0;

intptr_t *buffer = NULL;
size_t buffer_cap = 0;

void stack_push(intptr_t v) {{
stack_top++;
if(stack_top >= stack_cap) {{
stack_cap *= 2;
stack = realloc(stack, stack_cap * sizeof *stack);
}}
stack[stack_top] = v;
}}
intptr_t stack_pop() {{
intptr_t v = stack[stack_top];
stack_top--;
return v;
}}

void buffer_ensure(size_t size) {{
while(size >= buffer_cap) {{
buffer = realloc(buffer, buffer_cap*2 * sizeof *buffer);
memset(buffer + buffer_cap, 0, buffer_cap * sizeof *buffer);
buffer_cap *= 2;
}}
}}

int main() {{

memset(registers, 0, sizeof registers);

stack = malloc(16 * sizeof *stack);
stack_cap = 16;

buffer = calloc(16, sizeof *buffer);
buffer_cap = 16;

goto cbn_main;
""".format(num_registers=len(registers))

ops_template = """
cur_register = {reg};
value = registers[{reg}];
{body}
registers[{reg}] = value;
"""

line_template = '''
line_{lineid}:
    {body}
'''

ops_const = """
value = {value};
"""

ops_pre = {
    'i': '',
    'idx': 'value += stack_pop();',
    'cnt': 'value -= stack_pop();',
    'ptr': 'value = stack_pop();',
    'tbl': 'stack_push(value);buffer_ensure(value);value = buffer[value];',
    'x': 'stack_push(value); cur_register++; cur_register %= NUM_REGISTERS;\
            value = registers[cur_register];',
    'y': 'stack_push(value); cur_register += NUM_REGISTERS - 1; \
            cur_register %= NUM_REGISTERS; value = registers[cur_register];',
    'index': 'stack_push(0);',
    'pointer': 'stack_push(stack[stack_top]);',
    'table': 'do {{ intptr_t tmp = stack[stack_top]; \
            memmove(stack + stack_top - value + 1, \
            stack + stack_top - value + 2, (value - 1) * sizeof *stack); \
            stack[stack_top - value + 1] = tmp; }} while(0);',
    'buffer': 'value = getchar(); value = value != EOF ? value : 0;',
    'counter': 'value = &&{nextline};',
    'count': 'value = 1 - value;',
    'buf': 'do {{ intptr_t tmp = stack[stack_top]; \
            stack[stack_top] = value; value = tmp; }} while(0);',
    'cond': 'value = value < 0 ? -value : value;',
}
ops_post = {
    'i': '',
    'idx': 'value++;',
    'cnt': 'value--;',
    'ptr': 'stack_push(value);',
    'tbl': 'buffer_ensure(stack[stack_top]); \
            buffer[stack[stack_top]] = value; \
            value = stack_pop();',
    'x': 'registers[cur_register] = value; cur_register += NUM_REGISTERS - 1; \
            cur_register %= NUM_REGISTERS; value = stack_pop();',
    'y': 'registers[cur_register] = value; cur_register++; \
            cur_register %= NUM_REGISTERS; value = stack.pop();',
    'index': 'stack_pop();',
    'pointer': ops_pre['pointer'],
    'table': 'do { intptr_t tmp = stack[stack_top - value + 1]; \
            memmove(stack + stack_top - value + 1, \
            stack + stack_top - value + 2, value - 1); \
            stack[stack_top] = tmp; } while(0);',
    'buffer': 'putchar(value);',
    'counter': 'goto *value;',
    'count': 'value = -value',
    'buf': ops_pre['buf'],
    'cond': ops_pre['cond'],
}

def generate_op(args, op, pos):
    if isinstance(op, str):
        return (ops_pre if pos == 'prefix' else ops_post)[op].format(**args)
    else:
        return ops_const.format(value=op, **args)

def generate_ops(ast_entry, lineid, include_label=True):
    template_args = {
        'lineid': lineid,
        'nextline': lineid + 1,
        'reg': registers.index(ast_entry[1]),
    }
    gen_op = functools.partial(generate_op, template_args)
    body = '\n'.join(itertools.chain(
        map(gen_op, split_ops(ast_entry[0]), itertools.repeat('prefix')),
        map(gen_op, split_ops(ast_entry[2]), itertools.repeat('postfix')),
    ))
    body = ops_template.format(body=body, **template_args)
    if include_label:
        body = line_template.format(body=body, **template_args)
    return body

def generate_jmp(ast_entry, lineid):
    ast_entry = list(ast_entry)
    jmp_target = ast_entry.pop(0)
    return line_template.format(body=[
        'goto cbn_{target};',
        '{0} if(value > 0) goto cbn_{target};',
        'do { intptr_t cnd; {0} cnd = value; {1} \
                if(cnd && value) goto cbn_{target}; } while(0);',
        'do { intptr_t cnd1,cnd2; {0} cnd1 = value; {1} cnd2 = value; {2} \
                if((cnd1 && cnd2) || (!cnd1 && value)) goto cbn_{target}; \
                } while(0);',
    ][len(ast_entry)].format(
        *map(lambda entry: '\n'.join(
            map(lambda ops: generate_ops(ops, lineid, False), entry)
        ), ast_entry),
        target=jmp_target,
    ), lineid=lineid)

def generate(ast_entry, lineid):
    if isinstance(ast_entry, str):
        return "cbn_%s:line_%d:" % (ast_entry, lineid)
    elif isinstance(ast_entry, tuple):
        return generate_ops(ast_entry, lineid)
    elif isinstance(ast_entry, list):
        return generate_jmp(ast_entry, lineid)

generated = "\n".join(map(generate, ast, itertools.count()))

footer = """
do { } while(0);
}
"""

print(header, generated, footer, sep='\n')
