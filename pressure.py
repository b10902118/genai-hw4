from utils import *
from qa import *
from secret import api_keys
import time
import asyncio
import google.generativeai as genai
from tqdm import tqdm
import jinja2
import pickle
from random import shuffle
from datetime import datetime

# read prompt from prompt.txt
with open("./prompt.txt", "r") as f:
    prompt_template_str = f.read()
assert check_prompt(prompt_template_str)

environment = jinja2.Environment()
prompt_template = environment.from_string(prompt_template_str)
ans_template = environment.from_string(ans_template_str)

trial_num = 3
assert trial_num % 2 == 1, "Trial number should be odd"
test_num = 30
assert 0 < test_num <= test_num, "Invalid test number"
questions = questions[:test_num]

request_delay = 0.2  # best case can be 0
failed_delay = 2  # per question

# primitive key balancing
shuffle(api_keys)


async def process_question(q: str, model: genai.GenerativeModel, n: int) -> str:
    try:
        await asyncio.sleep(n * request_delay)
        # print(f"{n} sent")
        r = await model.generate_content_async(q)
        return r.text
    except:
        return None


async def trial() -> tuple[list[list[str]], list[list[str]]]:
    rationale_tests = []
    answer_tests = []

    for i in range(trial_num):
        print(f"Trial Solving {i+1}")
        failed = list(range(test_num))
        rationales = [""] * test_num

        genai.configure(api_key=api_keys[i])
        model = genai.GenerativeModel("gemini-pro")
        cnt = 0
        while failed:
            jobs = asyncio.gather(
                *[
                    process_question(
                        prompt_template.render(question=questions[j]), model, n
                    )
                    for n, j in enumerate(failed)
                ]
            )
            results = await jobs

            new_failed = []
            for j, r in zip(failed, results):
                if r is None:
                    # print(f"trial {i+1} question {j+1} failed")
                    new_failed.append(j)
                else:
                    rationales[j] = r

            if new_failed:
                print(f"Failed to generate content for {len(new_failed)} questions.")
                pre_cnt, cur_cnt = len(failed), len(new_failed)
                failed = new_failed

                cnt += 1
                if cnt > 2 and pre_cnt == cur_cnt:
                    cnt = 0
                    print(f"key {i} dead, swapping")
                    cur_i, nxt_i = i, (i + 1) % trial_num
                    api_keys[cur_i], api_keys[nxt_i] = (
                        api_keys[nxt_i],
                        api_keys[cur_i],
                    )
                    genai.configure(api_key=api_keys[i])
                    model = genai.GenerativeModel("gemini-pro")
                else:
                    sleep_time = len(failed) * failed_delay
                    print(f"sleep {sleep_time}")
                    time.sleep(sleep_time)
            else:  # no failed
                break

        rationale_tests.append(rationales)

    for i in range(trial_num):
        print(f"Trial Extracting {i+1}")
        failed = list(range(test_num))
        answers = [""] * test_num

        genai.configure(api_key=api_keys[i])
        model = genai.GenerativeModel("gemini-pro")
        # cnt = 1
        while failed:
            jobs = asyncio.gather(
                *[
                    process_question(
                        extract_prompt_fmt.format(
                            question=questions[j], rationale=rationale_tests[i][j]
                        ),
                        model,
                        n,
                    )
                    for n, j in enumerate(failed)
                ]
            )
            results = await jobs

            new_failed = []
            for j, r in zip(failed, results):
                if r is None:
                    # print(f"trial {i+1} extract {j+1} failed")
                    new_failed.append(j)
                else:
                    answers[j] = r

            if new_failed:
                print(f"Failed to extract answer for {len(new_failed)} questions.")
                pre_cnt, cur_cnt = len(failed), len(new_failed)
                failed = new_failed

                cnt += 1
                if cnt > 2 and pre_cnt == cur_cnt:
                    cnt = 0
                    print(f"key {i} dead, swapping")
                    cur_i, nxt_i = i, (i + 1) % trial_num
                    api_keys[cur_i], api_keys[nxt_i] = (
                        api_keys[nxt_i],
                        api_keys[cur_i],
                    )
                    genai.configure(api_key=api_keys[i])
                    model = genai.GenerativeModel("gemini-pro")
                else:
                    sleep_time = len(failed) * failed_delay
                    print(f"sleep {sleep_time}")
                    time.sleep(sleep_time)
            else:  # no failed
                break

        answer_tests.append(answers)
    return rationale_tests, answer_tests


start_time = time.time()
rationale_tests, answer_tests = asyncio.run(trial())
end_time = time.time()


# results to display
trials = [[0] * test_num for _ in range(trial_num)]
res_list = []
res_stats_str = ""

for i in range(trial_num):
    accurate_count = 0
    # Iterate over each example in the examples list.
    for j, (question, rationale, answer) in enumerate(
        zip(questions, rationale_tests[i], answer_tests[i])
    ):
        test_res = ""
        ## check result['answer'] not None
        if not answer_tests[i][j]:  # this should not happen
            print(f"answer_tests[{i}][{j}] is invalid")
            # trials[i].append(0) # not increase

            test_res += f"Trial {i+1}\n\n Skip question {j + 1}."
            test_res += "\n" + "<" * 6 + "=" * 30 + ">" * 6 + "\n\n"
            res_list.append(f"Trial {i+1}\n\n Skip question {j + 1}.")
            continue

        cleaned_result = clean_commas(answer_tests[i][j])
        # Q0, Q26 are not validated
        if find_and_match_floats(cleaned_result, answers[j]) or j in [0, 26]:
            trials[i][j] = 1
            accurate_count += 1

        test_res += f"Trial {i + 1}\n\n"
        test_res += f"Question {j + 1}:\n" + "-" * 20
        test_res += f"""\n\n{ans_template.render(question=prompt_template.render(question=question), rationale=rationale, answer=answer)}\n"""
        test_res += "\n" + "<" * 6 + "=" * 30 + ">" * 6 + "\n\n"
        res_list.append(test_res)

        # time.sleep(1)

    # Print the accuracy statistics.
    res_stats_str += f"Trial {i + 1}, accurate_count: {accurate_count}, total_count: {test_num}, accuracy: {accurate_count/ test_num * 100}%\n"

maj = trial_num // 2 + 1
sum_list = [sum(values) for values in zip(*trials)]
res_stats_str += (
    f"Final Accuracy: { sum(1 for n in sum_list if n > maj) / test_num * 100}%"
)

for res in res_list:
    print(res)
print("\n" + "=" * 20 + "\n")

for i, trial in enumerate(trials):
    print(f"{i}:", trial)

print("\n" + "=" * 20 + "\n")
print(res_stats_str)
pickle.dump(
    (prompt_template_str, trials, res_list, res_stats_str),
    open("result" + datetime.now().strftime("-%m-%d-%H-%M") + ".pkl", "wb"),
)

print(
    f"Time taken for {test_num} {'questions' if test_num>1 else 'question' }: {end_time - start_time} seconds"
)
