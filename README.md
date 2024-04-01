## Usage
Currently only CLI version
```bash
python pressure.py
```

## Setup
`secret.py` should contain at least 3 API keys from different google account:
```python
api_keys = [
    "key1",
    "key2",
    "key3",
    #the more the better
]
```

`prompt.txt` should contain your prompt

## Note
There seem to be other limits for api use, so it is possible to find one key dead even after pausing for a minute. 
Adapted from genai hw4. Big thanks to the TAs.
