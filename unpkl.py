import pickle
import glob

pkl_files = glob.glob("./*.pkl")

hard_cnt = [0] * 30

for filename in pkl_files:
    prompt_template_str, trials, res_list, res_stats_str = pickle.load(
        open(filename, "rb")
    )
    print(filename)
    print(res_list[7])

"""
    print(res_stats_str)
    sum_list = [sum(values) for values in zip(*trials)]
    hard = [i for i, s in enumerate(sum_list) if s < 2]
    for h in hard:
        hard_cnt[h] += 1
    print(hard)
    # for trial in trials:
    #    print(trial)
for i, cnt in enumerate(hard_cnt):
    print(f"{i}:", cnt)
"""
