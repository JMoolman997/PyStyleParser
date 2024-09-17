C Code Style Formatter

This project is a C code style formatter and checker that parses and formats C source code based on predefined style rules. It is built using Python, leveraging the pycparser library to parse C code and enforce consistent style conventions.
Features

    C Code Formatting: Automatically formats C source code according to style rules, such as indentation, placement of braces, spacing around operators, and function definitions.
    Comment Preservation: Extracts, preserves, and reinserts comments and macros while formatting the code.
    Preprocessor Handling: Extracts and reinserts preprocessor directives like #define and #include without altering their formatting.
    Support for Various C Constructs: Handles arrays, functions, pointers, structs, and more while ensuring consistent formatting.
    Indentation with Tabs: Formats the code using tabs for indentation as per the specified style guide.

Style Rules

    Opening Brace Placement: Opening braces for functions are placed on a new line, flush with the left margin.
    Single Space After Keywords: if, for, and while statements are followed by a single space before the opening parenthesis.
    No Spaces Inside Parentheses or Brackets: There are no spaces inside parentheses and array brackets.
    Consistent Indentation: Code is indented using tabs.
    No Spaces Before Function Call Parentheses: No spaces are allowed between function names and their parameter list.
    Operators Spacing: Additive operators (+, -) must have spaces on both sides, while multiplicative operators (*, /, %) can have spaces or not.
    Line Length: Ensures that no line exceeds 80 characters.

Requirements

    Python 3.6+
    pycparser library (for C code parsing)

Installing Dependencies

To install the necessary dependencies, run:

bash

pip install pycparser

Usage

You can use this tool to format C code files by providing the input and output file names as arguments.
Basic Usage

bash

python style_parser.py <input_file> <output_file>

For example:

bash

python style_parser.py test.c formatted_test.c

This will format the contents of test.c and save the output in formatted_test.c.
How It Works

    Preprocessing: The tool uses the C preprocessor (cpp) to process preprocessor directives.
    Parsing and Formatting: The tool parses the code using pycparser and applies custom formatting rules.
    Reinsertion of Comments and Macros: After formatting, comments and macros are reinserted into their original positions while maintaining proper indentation.
    Final Output: The formatted code is written to the specified output file.

Example

Before formatting:

c

#include <stdio.h>
// This function adds two integers
int add ( int a , int b ) { return a+b; }

int main(){
    printf("%d\n", add(2 ,3));
    return 0;
}

After formatting:

c

#include <stdio.h>

// This function adds two integers
int add(int a, int b)
{
    return a + b;
}

int main()
{
    printf("%d\n", add(2, 3));
    return 0;
}

Customization

The tool uses a CustomCGenerator class to define specific style rules. If you need to modify the style conventions, you can adjust the methods in this class.
Error Handling

    If the input code contains syntax errors, the tool will attempt to preserve the original code and output a message indicating where the error occurred.

License

This project is open-source and available under the MIT License.
