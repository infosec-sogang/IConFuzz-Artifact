import sys, os, csv
from itertools import combinations
from scipy.stats import mannwhitneyu
import statistics
from common import SC, EL, IB, TOTAL_TIME


def load_csv(csv_path):
    tool_name = os.path.splitext(os.path.basename(csv_path))[0]

    bug_rows = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        has_func = 'func' in headers

        for row in reader:
            ttes = []
            it = 1
            while True:
                col = 'iter_%d' % it
                if col not in row:
                    break
                val = row[col]
                ttes.append(None if val == 'N/A' else int(val))
                it += 1
            entry = {
                'contract': row['contract'],
                'bug_type': row['bug_type'],
                'func':     row.get('func', None),
                'tte':      ttes
            }
            bug_rows.append(entry)

    return tool_name, bug_rows


def load_multiple_csvs(csv_paths):
    all_data  = {}  # tool_name -> {(contract, bug_type, func): [tte, ...]}
    iter_cnts = {}  # tool_name -> iter_cnt

    for path in csv_paths:
        tool_name, rows = load_csv(path)
        all_data[tool_name] = {
            (r['contract'], r['bug_type'], r.get('func')): r['tte']
            for r in rows
        }
        iter_cnts[tool_name] = len(rows[0]['tte']) if rows else 0

    tool_names = list(all_data.keys())

    all_bug_keys = set()
    for data in all_data.values():
        all_bug_keys.update(data.keys())
    all_bug_keys = sorted(all_bug_keys)
    max_iter = max(iter_cnts.values())

    bug_rows = []
    for (contract, bug_type, func) in all_bug_keys:
        entry = {
            'contract': contract,
            'bug_type': bug_type,
            'func':     func,
            'tte':      {}
        }
        for name in tool_names:
            entry['tte'][name] = all_data[name].get(
                (contract, bug_type, func),
                [None] * iter_cnts.get(name, max_iter)
            )
        bug_rows.append(entry)

    return tool_names, bug_rows


def get_final_counts(bug_rows, tool_name):
    if not bug_rows:
        return []
    iter_cnt = len(bug_rows[0]['tte'][tool_name])
    counts = []
    for it in range(iter_cnt):
        n = sum(1 for row in bug_rows
                if row['tte'][tool_name][it] is not None)
        counts.append(n)
    return counts


def vargha_delaney_a12(a, b):
    m, n = len(a), len(b)
    more = sum(1 for x in a for y in b if x > y)
    tie  = sum(1 for x in a for y in b if x == y)
    return (more + 0.5 * tie) / (m * n)


def run_statistical_tests(label, tool_names, counts_per_tool):
    n_tools = len(tool_names)

    print("\n[%s]" % label)
    print("  %-15s  %8s  %8s  %8s"
          % ("Tool", "Mean", "Median", "Std"))
    print("  " + "-" * 50)
    for name, counts in zip(tool_names, counts_per_tool):
        avg = sum(counts) / len(counts)
        med = statistics.median(counts)
        std = statistics.stdev(counts)
        print("  %-15s  %8.2f  %8.1f  %8.2f" % (name, avg, med, std))

    pairs   = [(0, j) for j in range(1, n_tools)]

    print("\n  %-15s  %-15s  %6s  %6s"
          % ("Tool A", "Tool B", "p-value", "A12"))
    print("  " + "-" * 55)

    for (i, j) in pairs:
        a, b  = counts_per_tool[i], counts_per_tool[j]
        _, p  = mannwhitneyu(a, b, alternative='two-sided')
        p     = max(p, 1e-300)
        a12   = vargha_delaney_a12(a, b)
        print("  %-15s  %-15s  %7.4f  %6.4f"
              % (tool_names[i], tool_names[j], p, a12))


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <Data A.csv> <Data B.csv> ..." % sys.argv[0])
        sys.exit(1)

    csv_paths  = sys.argv[1:]
    tool_names, bug_rows = load_multiple_csvs(csv_paths)

    print("=" * 60)
    print("Tools     : %s" % ", ".join(tool_names))
    print("Bug cases : %d" % len(bug_rows))
    print("Iterations: %d" % len(bug_rows[0]['tte'][tool_names[0]]))
    print("=" * 60)

    counts_per_tool = [get_final_counts(bug_rows, name) for name in tool_names]
    label = os.path.commonprefix([os.path.basename(p) for p in csv_paths]).strip('_')
    run_statistical_tests(label or "MWU", tool_names, counts_per_tool)


if __name__ == "__main__":
    main()