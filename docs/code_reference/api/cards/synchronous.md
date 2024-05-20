# Cards Synchronous Endpoints

This `Cards` endpoint provides methods to interact with the cards of the authenticated user.

Example usage of the Cards endpoint object:

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    cards = client.Cards.get_all_cards()
    print(cards)
```

---

::: pyrevolut.api.cards.endpoint.EndpointCardsSync

---
