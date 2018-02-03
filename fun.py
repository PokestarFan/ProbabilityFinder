from tqdm import tqdm
from subprocess import run, PIPE

for i in tqdm(range(1000)):
	run('cmd.exe /C probability.py {}'.format(i+2))