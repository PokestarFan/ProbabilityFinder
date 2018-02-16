import os
from shutil import rmtree as rm
from tqdm import tqdm

dirs = [x for x in os.listdir() if not os.path.isfile(x)]
for i in tqdm(range(len(dirs))):
    x = dirs[i]
    os.chdir(x)
    bad_dirs = [y for y in os.listdir() if not os.path.isfile(y)]
    if len(bad_dirs) > 0:
        for j in tqdm(range(len(bad_dirs))):
            y = bad_dirs[j]
            rm(y)
            cwd = os.getcwd()
            print('Deleted folder '+cwd+'\\Probability')
    os.chdir('..')