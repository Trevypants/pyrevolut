# Webhooks Asynchronous Endpoints

This `Webhooks` endpoint provides asynchronous methods to interact with the webhooks of the authenticated user.

Example usage of the Webhooks endpoint object:

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
        webhooks = await client.Webhooks.get_all_webhooks()
        print(webhooks)

asyncio.run(run())
```

---

::: pyrevolut.api.webhooks.endpoint.EndpointWebhooksSync

---
