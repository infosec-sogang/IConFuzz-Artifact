import sys, os
from common import init_io_cve_info, print_median_time
from common import IB
from plot_IO_cve import analyze_dir

def main():
    if len(sys.argv) < 2:
        print("Usage: %s [result dir]" % sys.argv[0])
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
                
    print_median_time(IB, targ_list, time_map_list)

if __name__ == "__main__":
    main()