## Usage
Currently only CLI version
```bash
python pressure.py
```

sample output
```
Trial 1
Rationale
use key 0
Extract
use key 1
Trial 2
Rationale
use key 2
====================
... (interaction log)
====================

0: [1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
1: [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
2: [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

====================

Trial 1, accurate_count: 23, total_count: 30, accuracy: 76.66666666666667%
Trial 2, accurate_count: 23, total_count: 30, accuracy: 76.66666666666667%
Trial 3, accurate_count: 22, total_count: 30, accuracy: 73.33333333333333%
Final Accuracy: 70.0%
Time taken for 30 questions: 208.38231706619263 seconds
```

## Setup
`secret.py` should contain at least 3 API keys from different google accounts:
```python
api_keys = [
    "key1",
    "key2",
    "key3",
    #the more the better
]
```
`param.py` should contain all the following variables defined:
```python
trial_num = 3
assert trial_num % 2 == 1, "Trial number should be odd"
test_num = 30
assert 0 < test_num <= test_num, "Invalid test number"

request_delay = 0.5  # best case can be 0
failed_delay = 1  # per question
```

`prompt.txt` should contain your prompt

## Note
There seem to be other limits for api use, so it is possible to find one key dead even after pausing for a minute. 
Adapted from genai hw4. Big thanks to the TAs.
