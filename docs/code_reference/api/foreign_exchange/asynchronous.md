# Foreign Exchange Asynchronous Endpoints

This `Foreign Exchange` endpoint provides asynchronous methods to interact with the foreign exchange of the authenticated user.

Example usage of the Foreign Exchange endpoint object:

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
        rate = await client.ForeignExchange.get_exchange_rate(
            from_currency="USD",
            to_currency="EUR",
            amount=1.0,
        )
        print(rate)

asyncio.run(run())
```

---

::: pyrevolut.api.foreign_exchange.endpoint.EndpointForeignExchangeAsync

---
