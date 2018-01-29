from __future__ import absolute_import, division, print_function
from random import randrange
import os
from tqdm import tqdm

def write_to_csv(filename, *args, newline = True):
    write_string = ''
    for arg in args:
        if type(arg) == list:
            for i in arg:
                write_string += str(i) + ','
        else:
            write_string += str(arg) + ','
    if newline:
        write_string = write_string.rstrip(',') + '\n'
    else:
        write_string = write_string.rstrip(',')
    with open(filename+'.csv', 'a') as file:
        file.write(write_string)

def move_dir(dirname, parent = False):
    if not parent:
        dirname = str(dirname)
        exists = os.path.isfile(dirname)
        try:
            os.mkdir(dirname)
            os.chdir(dirname)
        except FileExistsError:
            os.chdir(dirname)
    else:
        os.chdir("..")

def calculate_probability(odds):
    file_count = 0
    move_dir('Probability')
    move_dir(str(odds))
    d = {}
    writelist = []
    percentlist = []
    for i in tqdm(range(odds)):
        d[str(i)] = 0
        writelist.append(f'Times {i}')
        percentlist.append(f'Percent {i}')
    while True:
        if os.path.isfile(str(file_count)+'.csv'):
            file_count += 1
        else:
            break
    filename = str(file_count)
    write_to_csv(filename, 'Number', 'Value')
    for i in tqdm(range(500 * odds)):
        ran = randrange(odds)
        ran = int(ran)
        d[str(ran)] += 1
        if i == 999:
            write_to_csv(filename, i, ran+1, newline = False)
        else:
            write_to_csv(filename, i, ran+1)
    writelist2 = []
    for i in d:
        writelist2.append(d[i])
    percentlist2 = []
    for i in writelist2:
        percentlist2.append(round(((i/1000)*100), 2))
    if os.path.isfile('runs.csv'):
        write_to_csv('runs', file_count, writelist2, percentlist2)
    else:
        write_to_csv('runs', 'Run #', writelist, percentlist)
        write_to_csv('runs', file_count, writelist2, percentlist2)

def run_tests(times, odds):
    for i in tqdm(range(times)):
        calculate_probability(odds)
        os.chdir("..")
        os.chdir("..")


def get_input(times = True, odds = True):
    if times:
        times = input('How many times?')
    if odds:
        odds = input('The odds?')
    run_tests(times, odds)
