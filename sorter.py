from os import getcwd, listdir, mkdir, rename
from os.path import join, isdir
from shutil import rmtree, copytree

def test_case_len(path):
    data = []
    with open(join(path, "input.txt")) as file:
        data.append(len(file.readlines()))
    return data

cwd = getcwd()

files_path = join(cwd, 'files')

parts =  sorted(listdir(files_path))

last_part_path = join(files_path, parts[-1])

testcases = [(t, test_case_len(join(last_part_path, t))) for t in listdir(last_part_path)]
sorted_testcases = sorted(testcases, key=lambda x: x[1])

buffer_dir = join(cwd, "buffer")

if isdir(buffer_dir):
    rmtree(buffer_dir)
mkdir(buffer_dir)

for part in parts[:5]:
    origin = join(files_path, part)
    dest = join(buffer_dir, part)
    copytree(origin, dest)

for part in parts[5:]:
    mkdir(join(buffer_dir, part))
    for i, test in enumerate(sorted_testcases, start=0):
        origin = join(files_path, part, test[0])
        if i % 2:
            dest = join(buffer_dir, part, str(26 + (i// 2)))
        else:
            dest = join(buffer_dir, part, str(1 + i // 2))
        copytree(origin, dest)

rmtree(files_path)
rename(buffer_dir, files_path)