# Transfers Synchronous Endpoints

This `Transfers` endpoint provides methods to interact with the transfers of the authenticated user.

Example usage of the Transfers endpoint object:

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    reasons = client.Transfers.get_transfer_reasons()
    print(reasons)
```

---

::: pyrevolut.api.transfers.endpoint.EndpointTransfersSync

---
