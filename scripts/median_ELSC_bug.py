import os
import sys

from common import EL, SC, collect_found_times, init_elsc_bug_info
from plot_ELSC_bug import analyze_dir, classify_targets


def print_median_time(bug_sig, targ_list, time_map_list, bug_info):
    iter_cnt = len(time_map_list)
    for targ in targ_list:
        found_times = collect_found_times(bug_sig, time_map_list, targ)
        found_times.sort()
        func_list = bug_info[targ]
        func_list = {func: [] for (sig, func) in func_list if bug_sig == sig and func is not None}
        for found_time in found_times:
            for (func, time) in found_time:
                if func not in func_list: func_list[func] = [time]
                else: func_list[func].append(time)

        for func in func_list:
            found_times = func_list[func]
            if len(found_times) <= iter_cnt/2:
                print("%s ( %s ) : N/A" % (targ, func))
            else:
                sec = ", ".join(map(str, found_times))
                print("%s ( %s ): %.2f" % (targ, func, found_times[iter_cnt//2]))

def main():
    if len(sys.argv) < 2:
        print("Usage: %s [result dir]" % sys.argv[0])
        exit(1)

    bug_info = init_elsc_bug_info(SC, EL)
    target_dirs = sys.argv[1:]
    iter_cnt = len(os.listdir(target_dirs[0]))
    target_dirs.sort()

    time_map_list = []
    for iter in range(1, iter_cnt + 1):
        time_map = {}
        for targ_dir in target_dirs:
            analyze_dir(bug_info, targ_dir, iter, time_map)
        time_map_list.append(time_map)

    targ_list = [ (targ_dir.split('/')[-2]
                if targ_dir.endswith('/') else targ_dir.split('/')[-1])
                for targ_dir in target_dirs ]

    SC_list, EL_list = classify_targets(bug_info, targ_list)
    print_median_time(SC, SC_list, time_map_list, bug_info)
    print("===================================")
    print_median_time(EL, EL_list, time_map_list, bug_info)
    print("===================================")

if __name__ == "__main__":
    main()
