# Foreign Exchange Synchronous Endpoints

This `Foreign Exchange` endpoint provides methods to interact with the foreign exchanges of the authenticated user.

Example usage of the Foreign Exchange endpoint object:

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    rate = client.ForeignExchange.get_exchange_rate(
        from_currency="USD",
        to_currency="EUR",
        amount=1.0,
    )
    print(rate)
```

---

::: pyrevolut.api.foreign_exchange.endpoint.EndpointForeignExchangeSync

---
