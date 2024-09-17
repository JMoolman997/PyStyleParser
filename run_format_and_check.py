import os
import sys
import subprocess
from style_parser import format_c_code

# Paths
test_in_dir = './test_in'
current_dir = '.'
style_check_script = 'style_check.py'

# List of test files
test_files = [
    'test.c',
    'test_nested_struct.c',
    'test_struct.c',
    'test_struct_function.c',
    'test_switch.c',
    'test_switch_while.c',
    'test_while.c'
]

def format_file(input_file, output_file):
    """Formats a single C file from input_file and writes the result to output_file."""
    with open(input_file, 'r') as f:
        code = f.read()

    formatted_code = format_c_code(code)

    with open(output_file, 'w') as f:
        f.write(formatted_code)

    print(f"Formatted code written to {output_file}")

def format_all_files():
    """Formats all the test case files and writes them to the current folder."""
    formatted_files = []
    for test_file in test_files:
        input_file = os.path.join(test_in_dir, test_file)
        output_file = os.path.join(current_dir, test_file)

        # Format the file
        format_file(input_file, output_file)
        formatted_files.append(output_file)

    return formatted_files

def run_style_check():
    """Runs the style check script."""
    try:
        subprocess.run(['python', style_check_script], check=True)
        print("Style check completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Style check failed: {e}")

def cleanup_files(files):
    """Removes the formatted files after the style check."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed file: {file}")

def main():
    # Step 1: Format all the files
    formatted_files = format_all_files()

    # Step 2: Run style_check.py
    run_style_check()

    # Step 3: Clean up formatted files
    #cleanup_files(formatted_files)

if __name__ == "__main__":
    main()

