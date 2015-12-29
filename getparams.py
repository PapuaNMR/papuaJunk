import re
filename = 'fdatap.h'
pattern  = r"\#define\s+(FD\w+)\s+(\d+)"
new_file = []

# Make sure file gets closed after being iterated
with open(filename, 'r') as f:
   # Read the file contents and generate a list with each line
   lines = f.readlines()

# Iterate each line
for line in lines:

    # Regex applied to each line 
    match = re.match(pattern, line)
    if match:
        # Make sure to add \n to display correctly when we write it back
        new_line = '\''+match.group(1)+': '+match.group(2)+'\',' 
        print new_line
        new_file.append(new_line+'\n')

with open(filename+'.out', 'w') as f:
     # go to start of file
     f.seek(0)
    # actually write the lines
     f.writelines(new_file)
