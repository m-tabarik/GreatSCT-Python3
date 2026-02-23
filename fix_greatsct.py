import os
import re

# Fix orchestra.py
orchestra_file = 'lib/common/orchestra.py'
with open(orchestra_file, 'r') as f:
    content = f.read()

# Replace the import
content = content.replace('import imp', 'import importlib.util')

# Replace imp.load_source with importlib equivalent
def replace_load_source(match):
    indent = match.group(1)
    var_name = match.group(2)
    path = match.group(3)
    
    return f'''{indent}spec = importlib.util.spec_from_file_location("{var_name}", {path})
{indent}{var_name} = importlib.util.module_from_spec(spec)
{indent}spec.loader.exec_module({var_name})'''

# Use regex to find and replace imp.load_source patterns
pattern = r'(\s+)(\w+)\s*=\s*imp\.load_source\s*\(\s*[\'"][^\'"]+[\'"]\s*,\s*([^)]+)\s*\)'
content = re.sub(pattern, replace_load_source, content)

with open(orchestra_file, 'w') as f:
    f.write(content)

print("Fixed orchestra.py")

# Also check for other files using imp
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and file != 'fix_greatsct.py':
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                py_content = f.read()
            
            if 'import imp' in py_content:
                py_content = py_content.replace('import imp', 'import importlib.util')
                
                # Also try to fix load_source in this file
                if 'imp.load_source' in py_content:
                    py_content = re.sub(pattern, replace_load_source, py_content)
                
                with open(filepath, 'w') as f:
                    f.write(py_content)
                print(f"Fixed {filepath}")

print("All fixes applied!")
