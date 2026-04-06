import sys, os, csv
from itertools import combinations
from lifelines.statistics import logrank_test
from common import TOTAL_TIME


def load_csv(csv_path):
    tool_name = os.path.splitext(os.path.basename(csv_path))[0]

    bug_rows = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
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
    all_data  = {}
    iter_cnts = {}

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


def _median_tte(durations, events):
    n_total  = len(durations)
    n_found  = sum(events)

    if n_found < n_total / 2:
        return None

    found_times = sorted(d for d, e in zip(durations, events) if e)
    idx = int(n_total / 2) - (n_total - n_found)
    idx = max(0, min(idx, len(found_times) - 1))
    return found_times[idx]


def get_tte_arrays(bug_row, tool_name):
    census_time = TOTAL_TIME * 60
    ttes = bug_row['tte'][tool_name]
    durations = [t if t is not None else census_time for t in ttes]
    events    = [t is not None for t in ttes]
    return durations, events


def run_logrank_tests(tool_names, bug_rows):
    n_tools = len(tool_names)
    pairs   = [(0, j) for j in range(1, n_tools)]
    n_bugs  = len(bug_rows)

    print("\n[Log-rank Test]")
    print("  Total bug cases  : %d" % n_bugs)

    for (i, j) in pairs:
        name_a = tool_names[i]
        name_b = tool_names[j]

        sig_count = 0
        a_wins    = 0
        b_wins    = 0
        skipped   = 0

        for row in bug_rows:
            dur_a, evt_a = get_tte_arrays(row, name_a)
            dur_b, evt_b = get_tte_arrays(row, name_b)

            if not any(evt_a) and not any(evt_b):
                skipped += 1
                continue

            result = logrank_test(dur_a, dur_b,
                                  event_observed_A=evt_a,
                                  event_observed_B=evt_b)
            p     = max(result.p_value, 1e-300)

            if p < 0.05:
                sig_count += 1
                med_a = _median_tte(dur_a, evt_a)
                med_b = _median_tte(dur_b, evt_b)

                if med_a is None and med_b is None: pass 
                elif med_a is None: b_wins += 1 
                elif med_b is None: a_wins += 1
                elif med_a < med_b: a_wins += 1
                else: b_wins += 1

        valid = n_bugs - skipped
        print("  %-20s vs %-20s" % (name_a, name_b))
        print("    Valid cases      : %d / %d" % (valid, n_bugs))
        print("    Significant      : %d / %d (p < 0.05)" % (sig_count, valid))
        print("    %-12s faster : %d cases" % (name_a, a_wins))
        print("    %-12s faster : %d cases" % (name_b, b_wins))
        print()


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

    run_logrank_tests(tool_names, bug_rows)


if __name__ == "__main__":
    main()