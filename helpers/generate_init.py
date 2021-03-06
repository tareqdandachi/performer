from os import listdir
from os.path import isfile, join

dev_path = "performer"

find_folders = lambda path: {join(path, f) for f in listdir(path) if not isfile(join(path, f)) and "__" not in f}

find_files = lambda path: {join(path, f) for f in listdir(path) if isfile(join(path, f)) and "__" not in f and f not in {".DS_Store"}}

MAX_DEPTH = 10

def traverse_path(path, depth=0):

    FILES = {".": set()}

    if depth > MAX_DEPTH: raise RecursionError

    for folder in find_folders(path):
        FILES[folder] = traverse_path(folder, depth=depth+1)

    for file in find_files(path):
        FILES["."].add(file[len(dev_path):])

    return FILES

def generate_init(files):

    code  = "# GENERATED BY `generate_init.py`\n"
    code += "# __init__.py that imports all classes\n"

    for loop in files:

        # for i in loop:
        for i in files[loop]:

            code += "# " + loop[len(dev_path)+1:] + "\n\n"

            has_files = False

            for j in files[loop][i]:
                has_files = True
                if "_deprecated.py" not in j:
                    code += "from " + j.replace(".py", "").replace("/", ".") + " import *\n"

            if has_files: code += "\n\n"
            else: code += "#TODO: MODULE EMPTY!\n\n\n"

    with open(dev_path+"/__init__.py", 'w') as f:
        f.write(code)

    print("Updated " + dev_path+"/__init__.py")

files = traverse_path(dev_path)

print("\nFOUND:\n", files, end="\n\n\n")

generate_init(files)


