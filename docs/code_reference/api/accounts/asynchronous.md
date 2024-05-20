# Accounts Asynchronous Endpoints

This `Accounts` endpoint provides asynchronous methods to interact with the accounts of the authenticated user.

Example usage of the Accounts endpoint object:

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
        accounts = await client.Accounts.get_all_accounts()
        print(accounts)

asyncio.run(run())
```

---

::: pyrevolut.api.accounts.endpoint.EndpointAccountsAsync

---
