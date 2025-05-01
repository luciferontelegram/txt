import os
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace the filter expression
    pattern = r'filters\.command\(\[.*?\]\) *& *~filters\.edited'
    replacement = r'filters.command(\1)'
    
    # Use regex to find and replace
    modified_content = re.sub(pattern, lambda m: m.group(0).split('&')[0].strip(), content)
    
    if content != modified_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"Fixed: {file_path}")
    else:
        print(f"No changes: {file_path}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                fix_file(os.path.join(root, file))

# Fix the plugins directory
process_directory('plugins')

# Fix other Python files in the root
for file in os.listdir('.'):
    if file.endswith('.py'):
        fix_file(file)

print("All files processed!") 