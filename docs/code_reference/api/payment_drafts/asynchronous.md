# Payment Drafts Asynchronous Endpoints

This `Payment Drafts` endpoint provides asynchronous methods to interact with the payment drafts of the authenticated user.

Example usage of the Payment Drafts endpoint object:

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
        drafts = await client.PaymentDrafts.get_all_payment_drafts()
        print(drafts)

asyncio.run(run())
```

---

::: pyrevolut.api.payment_drafts.endpoint.EndpointPaymentDraftsAsync

---
