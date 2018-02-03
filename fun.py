from tqdm import tqdm
from subprocess import run, PIPE

for i in tqdm(range(1000)):
	try:
		run('cmd.exe /C probability.py {}'.format(i+2))
	except KeyboardInterrupt:
		print('User quit program')
		exit()