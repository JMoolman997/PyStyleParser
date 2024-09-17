# C Code Style Formatter

This project is a C code style formatter and checker that parses and formats C source code based on predefined style rules. It is built using Python, leveraging the `pycparser` library to parse C code and enforce consistent style conventions.

## Features

- **C Code Formatting**: Automatically formats C source code according to style rules, such as indentation, placement of braces, spacing around operators, and function definitions.
- **Comment Preservation**: Extracts, preserves, and reinserts comments and macros while formatting the code.
- **Preprocessor Handling**: Extracts and reinserts preprocessor directives like `#define` and `#include` without altering their formatting.
- **Support for Various C Constructs**: Handles arrays, functions, pointers, structs, and more while ensuring consistent formatting.
- **Indentation with Tabs**: Formats the code using tabs for indentation as per the specified style guide.

## Style Rules

1. **Opening Brace Placement**: Opening braces for functions are placed on a new line, flush with the left margin.
2. **Single Space After Keywords**: `if`, `for`, and `while` statements are followed by a single space before the opening parenthesis.
3. **No Spaces Inside Parentheses or Brackets**: There are no spaces inside parentheses and array brackets.
4. **Consistent Indentation**: Code is indented using tabs.
5. **No Spaces Before Function Call Parentheses**: No spaces are allowed between function names and their parameter list.
6. **Operators Spacing**: Additive operators (`+`, `-`) must have spaces on both sides, while multiplicative operators (`*`, `/`, `%`) can have spaces or not.
7. **Line Length**: Ensures that no line exceeds 80 characters.

## Requirements

- Python 3.6+
- `pycparser` library (for C code parsing)

### Installing Dependencies

To install the necessary dependencies, run:

```bash
pip install pycparser
