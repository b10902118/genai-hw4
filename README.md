Currently only CLI version
```bash
python pressure.py
```

`secret.py` should contain at least 3 API keys from different google account:
```python
api_keys = [
    "key1",
    "key2",
    "key3",
    #the more the better
]
```
There seem to be other limits for api use, so it is possible to find one key dead even after pausing for a minute. 
