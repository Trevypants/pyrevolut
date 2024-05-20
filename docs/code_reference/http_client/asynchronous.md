# PyRevolut Asynchronous Client

PyRevolut provides an asynchronous client that can be used to interact with the Revolut Business API.

Example initialization of the client object:

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

::: pyrevolut.client.asynchronous.AsyncClient

---
