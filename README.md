# C, But Not
A programming language that looks like C at first glance...but it's really, really not. Created for MoCoHacks 2021, by [CircuitCraft42](github.com/CircuitCraft42) and [joshop](github.com/joshop).

## Specification
C, But Not is a language with a syntax heavily inspired by C.

The semantics, however, are a totally different story.

A program is a list of *declarations* and *labels*.
A declaration looks like this:

```
"int" decl_name ";"
```

A label looks like this:

```
"int" label_name "()" "{"
  *body*
"}"
```

The body of a label is where your program's behavior is.
Before that, though, it's important to mention that labels are *not* functions,
despite them superficially resembling C functions.
When the end of a label is reached, control falls through to the next label
in source file order.

Now, the body of a label is a list of statements.
They are semicolon-terminated and have a couple different variants.

The first:

```
prefix eq_reg ( infix reg )* postfix ";"
```

*prefix* is a valid C identifier. Its meaning is described later.
*eq_reg* is a *reg* followed by a literal `=`, with no whitespace in between.
*postfix* is also an identifier. And it will likewise be described later.

If any repititions of the group exist, they are expanded into an equivalent
sequence of groupless instances of this construction like so:

1. Replace all instances of *reg* with the corresponding *eq_reg*,
   by appending `=`.
2. Add `prefix eq_reg infix$1 ";"` to the output, where `infix$1`
   is the first instance of *infix*.
3. Remove *prefix* and *eq_reg* from the statement.
4. Repeat steps 2-3 until the statement is no longer valid.

The second type of statement is:

```
label_name "(" ( argument ( "," argument )* )? ");"
```

*argument* is an instance of `prefix reg ( infix reg )* postfix`.

When there are no instances of *argument*, the program immediately
jumps to *label_name*. When there are, the arguments are converted into
type 1 statements, by substituting each *reg* for the corresponding *eq_reg*.
Then, the statements are executed in order, and the final value of each is
saved (if the statement was expanded, then the final value of the last
expanded statement is used instead).
If there is just one argument, the jump is performed if it is positive.
If there are two, the jump is performed if both are positive. If there are
three, then the jump is performed if either the first and second are both
positive, or the first is negative (or zero) and the third is positive.

### Operations, and registers

The program has access ten registers (listed below), an unbounded stack, and
an unbounded buffer which is initialized to zeroes. 
Now for the juicy part: how does the code actually run?

After being expanded, each statement consists of three parts: a prefix,
an eq\_reg, and a postfix. First things first, take the `=` back off the
register name. It's annoying. Now, the valid register names are:
`+`, `-`, `*`, `/`, `%`, `&`, `|`, `^`, `<<`, and `>>`, in that order.
When each statement is executed, the first step is that the register's
value is read. Then, it's passed into an operation pipeline, and the final
value is saved back into the register. How is the pipeline defined, you ask?
Why, by the prefix and postfix!

Each of prefix and postfix consists of a sequence of words,
separated\_by\_underscores or byCamelCase. Each word describes an operation,
depending on whether in appears in the prefix or postfix, and a single
integer value is passed from one operation to the next; the words are chosen to be similar to 
real programming concepts to enhance confusion. The result from
the prefix is passed to the postfix. the result from the postfix is saved into
the register.

Here's the current list of commands:

<table>
<tr><th>Word</th><th>Prefix</th><th>Postfix</th></tr>
<tr><td>i</td><td>Nop (Identity)</td><td>Nop (Identity)</td></tr>
<tr><td>idx</td><td>Pop and add</td><td>Add 1</td></tr>
<tr><td>cnt</td><td>Pop and subtract (value - stack)</td><td>Subtract 1</td></tr>
<tr><td>ptr</td><td>Pop stack</td><td>Push to stack</td></tr>
<tr><td>tbl</td><td>
Push the value to the stack, then use it as an index
into the buffer. Read buffer.
</td><td>
Pop the stack to get an index. Set the value into
the buffer at that index. Return the index.
</td></tr>
<tr><td>x</td><td>
Push the current value to the stack, then select
the next register. Read its value.
</td><td>
Save the current value into the selected register,
then select the previous register and pop the stack.
</td></tr>
<tr><td>y</td>
<td>Same as `x`, but select the previous register instead.</td>
<td>Same as `x`, but select the next register instead.</td></tr>
<tr><td>index</td>
<td>Push a zero onto the stack. Identity.</td>
<td>Pop the stack and discard. Identity.</td></tr>
<tr><td>pointer</td>
<td>Duplicate the top of the stack</td>
<td>Same as Prefix</td></tr>
<tr><td>table</td>
<td>Right rotate the stack (depth of value)</td>
<td>Left rotate the stack (depth of value)</td></tr>
<tr><td>buffer</td>
<td>Read a character from stdin.</td>
<td>Output a character to stdout.</td></tr>
<tr><td>counter</td>
<td>Get the current program location as an integer.</td>
<td>Jump to the line after where the program location was saved.</td></tr>
<tr><td>count</td><td>Logical NOT (subtract from 1)</td><td>Negation</td></tr>
<tr><td>buf</td><td>Swap value and top of stack</td><td>Same as Prefix</td></tr>
<tr><td>cond</td><td>Absolute value</td><td>Same as Prefix</td></tr>
</table>

### Executing programs
A source file (extension .c) can be executed using the Python 3 based interpreter by
supplying its name as a command line argument. One of the most unique components
of this language is also important to note at this stage: *a program must
be valid C (syntactically) in order to be valid C, But Not.* This is the reason
for the inclusion of declaration statements.

The `compiler.py` script translated C, But Not code into vanilla C99.
It communicates only via stdio, so you need to pipe in and out of it.
Using the `counter` operation requires gcc extensions.
