# Transactions Synchronous Endpoints

This `Transactions` endpoint provides methods to interact with the transactions of the authenticated user.

Example usage of the Transactions endpoint object:

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    transactions = client.Transactions.get_all_transactions()
    print(transactions)
```

---

::: pyrevolut.api.transactions.endpoint.EndpointTransactionsSync

---
