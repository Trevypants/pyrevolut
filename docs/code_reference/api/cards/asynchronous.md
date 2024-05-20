# Cards Asynchronous Endpoints

This `Cards` endpoint provides asynchronous methods to interact with the cards of the authenticated user.

Example usage of the Cards endpoint object:

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
        cards = await client.Cards.get_all_cards()
        print(cards)

asyncio.run(run())
```

---

::: pyrevolut.api.cards.endpoint.EndpointCardsAsync

---
