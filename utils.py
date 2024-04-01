import re

extract_prompt_fmt = "Q:{question}\nA:{rationale}\nThe answer to the original question is (a number only): "
ans_template_str = "Prompt with Question:\n\n{{question}}\n\n--------------------\n\nProblem-solving Process:\n\n{{rationale}}\n\n--------------------\n\nFinal Answer\n\n{{answer}}"


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
