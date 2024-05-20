# Accounts Synchronous Endpoints

This `Accounts` endpoint provides methods to interact with the accounts of the authenticated user.

Example usage of the Accounts endpoint object:

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

::: pyrevolut.api.accounts.endpoint.EndpointAccountsSync

---
