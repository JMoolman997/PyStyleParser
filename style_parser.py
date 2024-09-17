import sys
import textwrap
import re
import subprocess
from pycparser import c_parser, c_ast, c_generator

class CustomCGenerator(c_generator.CGenerator):

    def __init__(self):
        super().__init__()
        self.indent_char = '\t'  # Rule 18: Use tabs for indentation
        self.indent_level = 0

    def _make_indent(self):
        return self.indent_char * self.indent_level

    def _generate_stmt_list(self, stmts):
        return ''.join(self._generate_stmt(stmt) for stmt in stmts or [])

    def _generate_stmt(self, n, add_indent=False):
        """Generates a statement and handles indentation."""
        typ = type(n)

        # Add indentation if required
        if add_indent:
            self.indent_level += 1
        indent = self._make_indent()
        if add_indent:
            self.indent_level -= 1
        # Handle expressions that require a semicolon
        if typ in (
            c_ast.Decl, c_ast.Assignment, c_ast.Cast, c_ast.UnaryOp,
            c_ast.BinaryOp, c_ast.TernaryOp, c_ast.FuncCall, c_ast.ArrayRef,
            c_ast.StructRef, c_ast.Constant, c_ast.ID, c_ast.Typedef,
            c_ast.ExprList):
            return indent + self.visit(n) + ';\n'

        elif typ in (c_ast.Compound,):
            # No extra indentation required before the opening brace of a
            # compound - because it consists of multiple lines it has to
            # compute its own indentation.
            #
            return self.visit(n)
        # Default case
        return indent + self.visit(n) + '\n'

    def _generate_type(self, n, modifiers=[], emit_declname=True):
        return super(CustomCGenerator, self)._generate_type(n)

    def visit_Decl(self, n, no_type=False):

        s = ''
        if n.funcspec:
            s += ' '.join(n.funcspec) + ' '

        if n.storage:
            s += ' '.join(n.storage) + ' '

        if n.init:
            s += ' = ' + self.visit(n.init)

        if no_type:
            s += n.name
        else:
            s += self.visit(n.type)

        return s 

    def visit_FuncDecl(self, n):
        # Generate the return type
        return_type = self.visit(n.type)

        # Generate the parameter list
        if n.args:
            params = self.visit(n.args)
        else:
            params = ''

        # Concatenate return type, function name, and parameters without space before '('
        return f'{return_type}({params})'
    
    def visit_ArrayDecl(self, n):
        # Rule 12: No spaces inside brackets
        arr = self.visit(n.type)
        dim = self.visit(n.dim) if n.dim else ''
        return f'{arr}[{dim}]'
    
    def visit_PtrDecl(self, n):
        return '*' + self.visit(n.type)

    def visit_TypeDecl(self, n):
        s = ''
        if isinstance(n.type, c_ast.IdentifierType):
            s += ' '.join(n.type.names)
        else:
            s += self.visit(n.type)
        if n.declname:
            s += ' ' + n.declname
        return s
    
    def visit_FuncDef(self, n):
        # Rule 2: Function body opening brace on a new line, flush with the left margin
        decl = self.visit(n.decl)
        # puts opeening '{' flus with left margin 
        old_indent_level = self.indent_level
        self.indent_level = 0
        body = self.visit(n.body)
        self.indent_level = old_indent_level
        # Rule 17: Separate functions by at least one blank line
        return f'\n{decl}\n{body}\n'
    
    def visit_ParamList(self, n):
        params = ', '.join(self.visit(param) for param in n.params)
        return params

    def visit_FuncCall(self, n):
        # Rule 5: No spaces between function name and parentheses
        fref = self.visit(n.name)
        args = self.visit(n.args)
        return f'{fref}({args})'

    def visit_ExprList(self, n):
        # Rule 8: One space after commas
        return ', '.join(self.visit(expr) for expr in n.exprs)

    def visit_If(self, n):
        s = 'if ('
        if n.cond: s += self.visit(n.cond)
        s += ') '
        s += self._generate_stmt(n.iftrue, add_indent=False).lstrip()
        if n.iffalse:
            s += ' else '
            s += self._generate_stmt(n.iffalse, add_indent=False).lstrip()
        return s

    def visit_For(self, n):
        """Handle the formatting of for loops with a single space before the opening brace."""
        init = self.visit(n.init) if n.init else ''
        cond = self.visit(n.cond) if n.cond else ''
        next = self.visit(n.next) if n.next else ''
        s = f'for ({init}; {cond}; {next}) '  # Single space before the opening brace

        if isinstance(n.stmt, c_ast.Compound):
            s += self._generate_stmt(n.stmt, add_indent=False).lstrip()  # Handle the block body
        else:
            # Single-line body of the for loop
            s += '\n' + self._generate_stmt(n.stmt, add_indent=True)

        return s

    def visit_While(self, n):
        # Rule 6 and 10: Space after 'while', same line for ')' and '{'
        s = 'while (' + self.visit(n.cond) + ') '
        s += self._generate_stmt(n.stmt, add_indent=False).lstrip()
        return s

    def visit_DoWhile(self, n):
        s = 'do '
        s += self._generate_stmt(n.stmt, add_indent=False)
        s += ' while ( ' + self.visit(n.cond) + ' );'
        return s

    def visit_Switch(self, n):
        s = 'switch (' + self.visit(n.cond) + ') {\n'
        self.indent_level += 1
        s += self._generate_stmt_list(n.stmt.block_items)
        self.indent_level -= 1
        s += self._make_indent() + '}\n'
        return s

    def visit_Case(self, n):
        s = 'case ' + self.visit(n.expr) + ':\n'
        self.indent_level += 1
        s += self._generate_stmt_list(n.stmts)
        self.indent_level -= 1
        return s

    def visit_Default(self, n):
        s = 'default:\n'
        self.indent_level += 1
        s += self._generate_stmt_list(n.stmts)
        self.indent_level -= 1
        return s

    def visit_BinaryOp(self, n):
        lval_str = self._parenthesize_if(n.left,
                                         lambda d: not self._is_simple_node(d))
        rval_str = self._parenthesize_if(n.right,
                                         lambda d: not self._is_simple_node(d))

        # Rule 13: Additive operators must be separated by one space on each side
        # Rule 14: Multiplicative operators can have spaces or not

        op = f' {n.op} '
        return lval_str + op + rval_str

    def visit_UnaryOp(self, n):
        if n.op == 'sizeof':
            # Always parenthesize the argument of sizeof since it can be
            # a name.
            return 'sizeof(%s)' % self.visit(n.expr)
        else:
            operand = self._parenthesize_unless_simple(n.expr)
            if n.op == 'p++':
                return '%s++' % operand
            elif n.op == 'p--':
                return '%s--' % operand
            else:
                return '%s%s' % (n.op, operand)

    def visit_Return(self, n):
        s = 'return'
        if n.expr:
            s += ' ' + self.visit(n.expr)
        s += ';'
        return s

    def visit_Assignment(self, n):
        lval_str = self.visit(n.lvalue)
        rval_str = self.visit(n.rvalue)
        op = f' {n.op} '
        return f'{lval_str}{op}{rval_str}'

    def visit_Compound(self, n):
        # Rule 1: Opening brace on the same line
        # Rule 2: Function body handled separately
        if self.indent_level == 0:
            s = '{\n'
        else:
            s = self._make_indent() + '{\n'
        self.indent_level += 1
        s += self._generate_stmt_list(n.block_items)
        self.indent_level -= 1
        s += self._make_indent() + '}'
        if self.indent_level == 0:
            s += '\n'  # Add newline after top-level blocks
        return s

    def visit_Struct(self, n):
        s = 'struct'
        if n.name:
            s += ' ' + n.name
        if n.decls:
            s += ' {\n'
            self.indent_level += 1
            for decl in n.decls:
                s += self._make_indent() + self.visit(decl) + ';\n'
            self.indent_level -= 1
            s += self._make_indent() + '}'
        return s

    def visit_Enum(self, n):
        s = 'enum'
        if n.name:
            s += ' ' + n.name
        if n.values:
            s += ' {\n'
            self.indent_level += 1
            s += self._make_indent() + ',\n'.join(self.visit(value) for value in n.values.enumerators)
            self.indent_level -= 1
            s += '\n' + self._make_indent() + '}'
        return s

    def visit_ID(self, n):
        return n.name

    def visit_Constant(self, n):
        return n.value

    def visit_Cast(self, n):
        return f'({self.visit(n.to_type)}){self.visit(n.expr)}'

    def visit_ArrayRef(self, n):
        # Rule 12: No spaces between an opening parenthesis and the expression
        arr = self._parenthesize_unless_simple(n.name)
        sub = self.visit(n.subscript)
        return f'{arr}[{sub}]'

    def visit_StructRef(self, n):
        # Access struct members
        name = self.visit(n.name)
        field = self.visit(n.field)
        return f'{name}{n.type}{field}'

    def visit_TernaryOp(self, n):
        cond = self.visit(n.cond)
        iftrue = self.visit(n.iftrue)
        iffalse = self.visit(n.iffalse)
        return f'{cond} ? {iftrue} : {iffalse}'

    def visit_Enumerator(self, n):
        s = n.name
        if n.value:
            s += ' = ' + self.visit(n.value)
        return s

def extract_comments_and_macros(code):
    comments = []
    macros = []
    clean_code = []

    lines = code.split('\n')
    in_block_comment = False
    block_comment = []
    block_comment_start = 0

    for i, line in enumerate(lines):
        # Match macros (like #define, #include)
        macro_match = re.match(r'^\s*#.*', line)
        if macro_match:
            macros.append((i, line.strip()))
            clean_code.append('')  # Keep an empty line to retain structure
            continue

        # Match inline comments (code followed by //)
        inline_comment_match = re.search(r'(.*)(//.*)', line)
        if inline_comment_match:
            code_part = inline_comment_match.group(1).rstrip()  # Code before the comment
            comment_part = inline_comment_match.group(2).strip()  # Inline comment
            comments.append((i, comment_part))  # Store the comment with its line number
            clean_code.append(code_part)  # Add the code without the comment
            continue

        # Match single-line comments (//...)
        single_comment_match = re.match(r'^\s*//.*', line)
        if single_comment_match:
            comments.append((i, line.strip()))
            clean_code.append('')  # Keep an empty line to retain structure
            continue

        # Detect start of block comments (/** ... */ or /* ... */)
        if re.match(r'^\s*/\*.*', line):
            in_block_comment = True
            block_comment_start = i
            block_comment.append(line.strip())
            clean_code.append('')  # Keep an empty line to retain structure
            continue

        # Detect end of block comments
        if in_block_comment:
            block_comment.append(line.strip())
            clean_code.append('')  # Keep an empty line to retain structure
            if re.match(r'.*\*/\s*$', line):
                comments.append((block_comment_start, '\n'.join(block_comment)))
                in_block_comment = False
                block_comment = []
            continue

        # Add clean line without comments or macros
        clean_code.append(line)

    return '\n'.join(clean_code), comments, macros


def preprocess_code(input_file):
    preprocessed_file = 'preprocessed_input.c'
    subprocess.run(['cpp', '-E', input_file, '-o', preprocessed_file], check=True)
    with open(preprocessed_file, 'r') as f:
        return f.read()

def format_c_code(code):
    clean_code, comments, macros = extract_comments_and_macros(code)

    parser = c_parser.CParser()
    ast = parser.parse(clean_code)

    # Assuming CustomCGenerator handles formatting
    generator = CustomCGenerator()
    formatted_code = generator.visit(ast)

    return formatted_code, comments, macros

def extract_leading_whitespace(line):
    """Helper function to extract the leading whitespace of a line."""
    return re.match(r'\s*', line).group()

def reinsert_comments_and_macros(formatted_code, comments, macros):
    formatted_lines = formatted_code.split('\n')

    # Insert comments back into their original positions with proper indentation
    for pos, comment in comments:
        if pos < len(formatted_lines):
            # Get the indentation level of the line below the comment
            if pos + 1 < len(formatted_lines):
                # If there's a next line, use its indentation
                leading_whitespace = extract_leading_whitespace(formatted_lines[pos + 1])
            else:
                leading_whitespace = ''  # No line below, no indentation

            # For multi-line block comments, apply indentation to each line of the comment
            indented_comment_lines = []
            for line in comment.split('\n'):
                indented_comment_lines.append(leading_whitespace + line)
            
            # Replace the current line with the properly indented comment block
            formatted_lines[pos] = '\n'.join(indented_comment_lines)

    # Insert macros back into their original positions (without changing indentation)
    for pos, macro in macros:
        if pos < len(formatted_lines):
            formatted_lines.insert(pos, macro)

    return '\n'.join(formatted_lines)


def format_c_code_with_comments_and_macros(code):
    # Step 1: Extract comments and macros
    clean_code, comments, macros = extract_comments_and_macros(code)

    # Step 2: Format the clean code using pycparser
    parser = c_parser.CParser()
    try:
        ast = parser.parse(clean_code)
    except Exception as e:
        print(f"Error parsing code: {e}")
        return code  # Return original code if parsing fails

    generator = CustomCGenerator()  # Assuming this handles the actual formatting
    formatted_code = generator.visit(ast)

    # Step 3: Reinsert comments and macros back into the formatted code, with indentation
    final_code = reinsert_comments_and_macros(formatted_code, comments, macros)

    return final_code


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        code = f.read()

    formatted_code = format_c_code_with_comments_and_macros(code)

    with open(output_file, 'w') as f:
        f.write(formatted_code)

    print(f"Formatted code written to {output_file}")

if __name__ == "__main__":
    main()

