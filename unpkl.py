import pickle
import glob


hard_cnt = [0] * 30

data = []
for folder in [str(dir) for dir in range(10)]:
    pkl_files = glob.glob(folder + "/*.pkl")
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
        data.append(
            (
                filename[2:-4],
                prompt_template_str,
                trials,
                res_list,
                float(res_stats_str.rsplit(":", 1)[-1][:-1]),
            )
        )

data_dict = {}
for d in data:
    if d[0] in data_dict:
        data_dict[d[0]].append(d[1:])
    data_dict[d[0]] = [d[1:]]

acc_list = []
for filename, data in data_dict.items():
    acc = sum([d[3] for d in data]) / len(data)
    acc_list.append((filename, acc))

acc_list = sorted(acc_list, key=lambda x: x[1])
for acc in acc_list:
    print(acc[0], acc[1])


# avg of each question
avg = [0] * 30
l = 0
for filename, data in data_dict.items():
    for d in data:
        for trial in d[1]:
            l += 1
            for i, t in enumerate(trial):
                avg[i] += t

avg = [(i, a / l) for i, a in enumerate(avg)]

avg = sorted(avg, key=lambda x: x[1])
for a in avg:
    print(a[0], a[1])


# data = sorted(data, key=lambda x: x[4])
# for d in data:
#    print(d[0], len(d[1]), d[4])

"""
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
