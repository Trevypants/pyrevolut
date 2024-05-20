# Payout Links Asynchronous Endpoints

This `Payout Links` endpoint provides asynchronous methods to interact with the payout links of the authenticated user.

Example usage of the Payout links endpoint object:

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
        links = await client.PayoutLinks.get_all_payout_links()
        print(links)

asyncio.run(run())
```

---

::: pyrevolut.api.payout_links.endpoint.EndpointPayoutLinksAsync

---
