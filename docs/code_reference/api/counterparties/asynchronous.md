# Counterparties Asynchronous Endpoints

This `Counterparties` endpoint provides asynchronous methods to interact with the counterparties of the authenticated user.

Example usage of the Counterparties endpoint object:

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
        counterparties = await client.Counterparties.get_all_counterparties()
        print(counterparties)

asyncio.run(run())
```

---

::: pyrevolut.api.counterparties.endpoint.EndpointCounterpartiesAsync

---
