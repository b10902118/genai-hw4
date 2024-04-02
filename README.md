## Usage
Currently only CLI version
```bash
python pressure.py
```

sample output see `output.md`

## Setup
`secret.py` should contain at least 3 API keys (5 recommended for batch) from different google accounts:
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

### Processing
#### single prompt (testing)
`./prompt.txt` should contain your prompt
#### multiple prompts (batch)
put all the prompt files (.txt) with different names under `./to_eval`. The result will be stored at `./to_eval/{filename[:-4]}.pkl`

## Note
There seem to be other limits for api use, so it is possible to find one key dead even after pausing for a minute.

Adapted from genai hw4. Big thanks to the TAs.
