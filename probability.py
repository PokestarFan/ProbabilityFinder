from __future__ import absolute_import, division, print_function
from random import randrange
import os, argparse, time
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

def calculate_probability(odds, exitmode = False, low_cpu = False):
    try:
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
        rep = 500 * odds
        if rep > 10000:
            rep = 10000
        for i in tqdm(range(rep)):
            ran = randrange(odds)
            ran = int(ran)
            d[str(ran)] += 1
            if i == 999:
                write_to_csv(filename, i, ran+1, newline = False)
            else:
                write_to_csv(filename, i, ran+1)
            if low_cpu:
                time.sleep(0.01)
        writelist2 = []
        percentlist2 = []
        for i in tqdm(range(odds)):
            val = d[str(i)]
            writelist2.append(val)
            percentlist2.append(round(((val/rep)*100), 2))
        if os.path.isfile('runs.csv'):
            write_to_csv('runs', file_count, writelist2, percentlist2)
        else:
            write_to_csv('runs', 'Run #', writelist, percentlist)
            write_to_csv('runs', file_count, writelist2, percentlist2)
        if exitmode:
            exit()
    except(KeyboardInterrupt, SystemExit):
        if exitmode:
            os.remove(str(file_count)+'.csv')
            exit()
        else:
            try:
                os.system('cls')
                print('User/program interrupted, lauching shutdown mode...')
                os.remove(str(file_count)+'.csv')
                print('Finilizaing current trial...')
                os.chdir("..")
                os.chdir("..")
            except FileNotFoundError:
                exit()
            calculate_probability(odds, exitmode = True)

def run_tests(times, odds, low_cpu = False):
    for i in tqdm(range(times)):
        calculate_probability(odds, low_cpu = low_cpu)
        os.chdir("..")
        os.chdir("..")


if __name__ == '__main__':
    os.system('cls')
    parser = argparse.ArgumentParser(description='Run big batch tests to really find out probability.')
    parser.add_argument('--version', action = 'version', version = '1.0')
    parser.add_argument('odds', nargs = 1, type = int, metavar = 'Odds for probability', help = 'Select the odds for probability, for example 2 to choose from 1 and 2')
    parser.add_argument('-t', '--times', nargs = 1, type = int, metavar = 'Times Repeated', help = 'The number of times to be repeated, default 10.', default = 10)
    parser.add_argument('-l', '-cpu', '-lcpu', '-low' ,'--low_cpu', help = 'Use low cpu?', action = 'store_true')
    args = parser.parse_args()
    odds = (args.odds)[0]
    times = args.times
    cpu = args.low_cpu
    if type(times) == list:
        times = times[0]
    run_tests(times, odds, low_cpu = cpu)
