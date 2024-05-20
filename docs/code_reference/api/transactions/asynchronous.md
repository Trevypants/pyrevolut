# Transactions Asynchronous Endpoints

This `Transactions` endpoint provides asynchronous methods to interact with the transactions of the authenticated user.

Example usage of the Transactions endpoint object:

```python
import asyncio
from pyrevolut.client import AsyncClient

CREDS_JSON_LOC = "path/to/creds.json"

client = AsyncClient(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

async def run():
    async with client:
        transactions = await client.Transactions.get_all_transactions()
        print(transactions)

asyncio.run(run())
```

---

::: pyrevolut.api.transactions.endpoint.EndpointTransactionsAsync

---
