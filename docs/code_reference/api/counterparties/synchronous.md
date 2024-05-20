# Counterparties Synchronous Endpoints

This `Counterparties` endpoint provides methods to interact with the counterparties of the authenticated user.

Example usage of the Counterparties endpoint object:

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    counterparties = client.Counterparties.get_all_counterparties()
    print(counterparties)
```

---

::: pyrevolut.api.counterparties.endpoint.EndpointCounterpartiesSync

---
