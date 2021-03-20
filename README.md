# c-but-not
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
Before that, though, it's important to mention that labels are *not* functions.
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
saved. If there is just one argument, the jump is performed if it is positive.
If there are two, the jump is performed if both are positive. If there are
three, then the jump is performed if either the first and second are both
positive, or the first is negative (or zero) and the third is positive.

