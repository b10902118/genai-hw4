import pickle
import glob

pkl_files = glob.glob("./*.pkl")

hard_cnt = [0] * 30

data = {}

for filename in pkl_files:
    prompt_template_str, trials, res_list, res_stats_str = pickle.load(
        open(filename, "rb")
    )
    # print(res_list)
    # convert old format to new
    if isinstance(res_list[0], str):
        # Get the length of each part
        part_len = len(res_list) // 3
        # Split res_list into three equal parts
        res_list = [
            res_list[i : i + part_len] for i in range(0, len(res_list), part_len)
        ]
    data[filename] = (prompt_template_str, trials, res_list, res_stats_str)


while True:
    n = int(input("Number of problem to check: "))
    for filename, (
        prompt_template_str,
        trials,
        res_list,
        res_stats_str,
    ) in data.items():
        print(filename,'\n')
        for i in range(3):
            print(res_list[i][n])
            input("press enter to continue")

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
