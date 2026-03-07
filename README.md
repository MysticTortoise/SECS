# Simple Expression-Configuration Script
SECS is a simple meshing between a functional-style language and a configuration format.

It's syntax is inspired by the simplicity of .ini while still being standardized.

It is intended for configuration where certain variables may change depending on external settings. 
SECS was developed for use in [TeaPacket](https://github.com/TeaspoonStudios/TeaPacketModular) where assets may need
different settings based on platform settings.

## Syntax
A `.secs` file is comprised of statements separated by semicolons (`;`)  
Each statement begins with an identifier (a combination of english letters a-z or A-Z, digits 0-9, and `.` or `_`.)  
It is then followed by an `=` symbol, and then an expression.

### Data Types
All values in SECS are numbers.  
A value is considered "falsey" if it is 0. Otherwise, it is "truthy".

### Expressions
Expressions are a sequence of number literals and identifiers separated by operators.  
#### Operators:
- Any of the standard arithmetic operators (`+`, `-`, `*`, and `/`) behave exactly as you would expect.
- The Bang operator (`!`) can be used to invert an expression. If the expression is truthy, it becomes 0. If the expression is falsey, it becomes 1.
- The comparison operators (`==`, `!=`, `>`, `>=`, `<`, `<=`) will evaluate both sides and evaluate to 1 if the comparison is true, and 0 otherwise.
- The ternary/conditional operator (`?:`) as seen in many languages is also supported.
- Parentheses will group expressions accordingly.

### Arguments
`NOT IMPLEMENTED YET`  
Statements may optionally have parentheses, listing several literals that must be passed when referring to this expression.
When argument names clash with expression names, the argument name takes precedence.

### Example
```
foo = 2 + 3;
bar = 7 + foo * 10;
```
`foo` evaluates to 5
`bar` evaluates to 57.

Order does not matter. The following is parsed identically to the above:
```
bar = 7 + foo * 10;
foo = 2 + 3;
```

### Errors
Statements may not be redefined. A file containing two definitions for the same statement name is an error.

Statements may not recursively call each other in a loop. Calling a statement while it has already been called is an error.

## Predefined Statements
`NOT IMPLEMENTED YET`  
The real strength of SECS is that expressions may be defined ahead of time by the code reading the configuration file.  
This way, `.secs` files can depend on a given environment.

To do so, `TODO: ADD`

## Goals
SECS is designed to be as simple as possible. Any changes or additions to the language will only be made if doing so is deemed necessary for basic functionality.

If more advanced scripting capabilities are required, consider using a proper scripting language like Python instead.
Features like control flow and any form of state will not be added. SECS is intended to be functional and direct.