import time
from random import shuffle


class key_profile:
    def __init__(self, api_key):
        self.api_key = api_key
        # self.cnt = 0
        # self.last_use = 0.0
        self.dead = False

    # def __lt__(self, other):
    #    return self.last_use < other.last_use


class key_manager:
    def __init__(self, api_keys: list):
        self.keys = [key_profile(k) for k in api_keys]
        shuffle(self.keys)  # prevent from keeping testing with the first key
        self.size = len(self.keys)
        self.cur_i = -1

    def newest_key(self, dead=False) -> str:
        if dead:
            self.keys[self.cur_i].dead = True
            # check if all used
            if False not in [k.dead for k in self.keys]:
                print("Warning: all keys have died, sleep 60s")
                time.sleep(60)
                for k in self.keys:
                    k.dead = False
        # just round robin (ok in concurrent, but not in parallel)
        self.cur_i = (self.cur_i + 1) % self.size

        # for i in range(self.size):
        #    if self.keys[i].last_use < self.keys[self.cur_i].last_use:
        #        self.cur_i = i

        # self.keys[self.cur_i].last_use = time.time()
        # print(f"use key {self.cur_i}")
        return self.keys[self.cur_i].api_key

    # def __getitem__(self, i):
    #    return self.keys[i].api_key


safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
import re

extract_prompt_str = "Q:{{question}}\nA:{{rationale}}\nThe answer to the original question is (a number only): "
ans_template_str = "Prompt with Question:\n\n{{question}}\n\n--------------------\n\nProblem-solving Process:\n\n{{rationale}}\n\n--------------------\n\nFinal Answer\n\n{{answer}}"


def check_prompt(prompt: str):
    if len(prompt) > 1024:
        print("Invalid prompt (too long, >1024 tokens)")
        return False
    elif "{{question}}" not in prompt:
        prompt_ex = "You need to put a placeholder {{question}} in your prompt."
        print(prompt_ex)
        return False
    return True


def clean_commas(text):
    # This function finds all numeric sequences that could include commas, decimal points, or be part of a float,
    # and then decides whether to remove commas based on the context.
    def process_match(match):
        number = match.group(0)
        # If the number is part of a float (has a decimal point), we'll return it unchanged.
        if "." in number:
            return number
        # Otherwise, remove all commas, treating them as thousand separators.
        else:
            number_list = number.split(",")
            new_string = number_list[0]
            for i in range(1, len(number_list)):
                if len(number_list[i]) == 3:
                    new_string += number_list[i]
                else:
                    new_string += f",{number_list[i]}"
        return new_string

    # Regex explanation:
    # - \d+ matches one or more digits.
    # - (?:,\d+)* matches zero or more groups of a comma followed by one or more digits.
    # - (?:\.\d+)? optionally matches a decimal point followed by one or more digits, to catch floats.
    pattern = r"\d+(?:,\d+)*(?:\.\d+)?"
    return re.sub(pattern, process_match, text)


def find_and_match_floats(input_string, ground_truth):
    # Compile a regex pattern that matches floats and integers, including signed ones
    pattern = re.compile(r"[-+]?\d*\.\d+|[-+]?\d+")

    # Find all matches in the input string
    found_numbers = pattern.findall(input_string)

    # Convert found strings to floats
    found_floats = [float(num) for num in found_numbers]

    # Check if any of the found floats match the ground truth
    return ground_truth in found_floats
