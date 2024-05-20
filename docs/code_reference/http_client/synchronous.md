# PyRevolut Synchronous Client

PyRevolut provides a synchronous client that can be used to interact with the Revolut Business API.

Example initialization of the client object:

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    accounts = client.Accounts.get_all_accounts()
    print(accounts)
```

---

::: pyrevolut.client.synchronous.Client

---
