from __future__ import absolute_import, division, print_function
from numpy.random import randint as randrange
import os, argparse, time
from multiprocessing import Process, Manager

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

def calculate_probability(odds, low_cpu = 0):
    try:
        file_count = 0
        move_dir('Probability')
        move_dir(str(odds))
        d = {}
        writelist = []
        percentlist = []
        for i in range(odds):
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
        for i in range(rep):
            ran = randrange(odds)
            ran = int(ran)
            d[str(ran)] += 1
            if i == 999:
                write_to_csv(filename, i, ran+1, newline = False)
            else:
                write_to_csv(filename, i, ran+1)
            if low_cpu:
                time.sleep(0.01*float(low_cpu))
        writelist2 = []
        percentlist2 = []
        for i in range(odds):
            val = d[str(i)]
            writelist2.append(val)
            percentlist2.append(round(((val/rep)*100), 2))
        return (writelist, percentlist, writelist2, percentlist2)
    except(KeyboardInterrupt, SystemExit):
        try:
            os.remove(str(file_count)+'.csv')
        finally:
            exit()

def worker(odds, returndict, num, low_cpu = 0):
    returndict[f'write{num}'] = calculate_probability(odds, low_cpu = low_cpu)
    os.chdir("..")
    os.chdir("..")
    os.system('cls')

def run_tests(times, odds, low_cpu = 0, shutdown = False):
    print('Starting...')
    manager = Manager()
    return_dict = manager.dict()
    job_list = []
    for i in range(times):
        p = Process(target=worker, args=(odds,return_dict,i), kwargs = {'low_cpu' : low_cpu})
        job_list.append(p)
        p.start()

    try:
        for proc in job_list:
            proc.join()
    except KeyboardInterrupt:
        print('User quit program...')
        time.sleep(5)
        for proc in job_list:
            proc.join()
        exit()
    else:
        move_dir('Probability')
        move_dir(str(odds))
        if not os.path.isfile('runs.csv'):
            write_to_csv('runs', return_dict.values()[0][0], return_dict.values()[0][1])
        for value in return_dict.values():
            write_to_csv('runs', value[2], value[3])
        print('Done!')
    finally:
        if shutdown:
            os.system('shutdown /S /F /T 0 /hybrid')

if __name__ == '__main__':
    os.system('cls')
    parser = argparse.ArgumentParser(description='Run big batch tests to really find out probability.')
    parser.add_argument('--version', action = 'version', version = '1.0')
    parser.add_argument('odds', nargs = 1, type = int, metavar = 'Odds for probability', help = 'Select the odds for probability, for example 2 to choose from 1 and 2')
    parser.add_argument('-t', '--times', nargs = 1, type = int, metavar = 'Times Repeated', help = 'The number of times to be repeated, default 10.', default = 10)
    parser.add_argument('-l', '-cpu', '-lcpu', '-low' ,'--low_cpu', help = 'Use low cpu mode. Specify amount', metavar = 'lowcpu', nargs = 1, default = 0)
    parser.add_argument('-s', '-shut', '--shutdown', help = 'Shuts down computer after trails are done.',dest = 'shut', action = 'store_true')
    args = parser.parse_args()
    odds = (args.odds)[0]
    times = args.times
    cpu = args.low_cpu
    shutdown = args.shut
    if type(cpu) == list:
        cpu = cpu[0]
    if type(times) == list:
        times = times[0]

    if times > 20:
        reps = round(times/10)
        for i in range(reps):
            run_tests(10, odds, low_cpu = cpu, shutdown = shutdown)
