import sys, os
from common import init_io_cve_info
from common import read_log_file, parse_fuzz_log
from common import print_found_time, plot_count_over_time
from common import IB

def analyze_targ(cve_points, result_dir, name, iter, time_map):
    targ = '%s-%d' % (name, iter)
    buf = read_log_file(result_dir, targ)
    found_times = []
    for (bug_sig, cve_pc) in cve_points:
        alarm_sig = "%s at %x" % (bug_sig, int(cve_pc, 16))
        found_time = parse_fuzz_log(buf, alarm_sig)
        if found_time is not None:
            found_times.append(found_time)

    if len(found_times) != 0:
        time_map[(name, bug_sig)] = min(found_times)

def analyze_dir(cve_info, targ_dir, iter, time_map):
    target_name = targ_dir.split('/')[-2] if targ_dir.endswith('/') else targ_dir.split('/')[-1]
    cve_points = cve_info[target_name]
    analyze_targ(cve_points, targ_dir, target_name, iter, time_map)

def print_found_count(time_map_list):
    found_sets = list(map(lambda m: set(m.keys()), time_map_list))
    found_always_n = len(set.intersection(*found_sets))
    found_at_least_once_n = len(set.union(*found_sets))
    found_min_n = min(map(len, found_sets))
    found_max_n = max(map(len, found_sets))
    print("%d bugs were found all the time" % found_always_n)
    print("%d bugs were found at least once" % found_at_least_once_n)
    print("At least %d bugs were found in each run" % found_min_n)
    print("At most %d bugs were found in each run" % found_max_n)

def main():
    if len(sys.argv) < 2:
        print("Usage: %s [result dirs ...]" % sys.argv[0])
        exit(1)

    cve_info = init_io_cve_info(IB)
    target_dirs = sys.argv[1:]
    iter_cnt = len(os.listdir(target_dirs[0]))
    target_dirs.sort()

    time_map_list = []
    for iter in range(1, iter_cnt + 1):
        time_map = {}
        for targ_dir in target_dirs:
            analyze_dir(cve_info, targ_dir, iter, time_map)
        time_map_list.append(time_map)
    
    targ_list = [ (targ_dir.split('/')[-2] 
                if targ_dir.endswith('/') else targ_dir.split('/')[-1]) 
                for targ_dir in target_dirs ]
    
    print_found_time(IB, targ_list, time_map_list)
    print("===================================")
    plot_count_over_time([IB], time_map_list)
    print("===================================")
    print_found_count(time_map_list)

if __name__ == "__main__":
    main()
