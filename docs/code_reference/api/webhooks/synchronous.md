# Webhooks Synchronous Endpoints

This `Webhooks` endpoint provides methods to interact with the webhooks of the authenticated user.

Example usage of the Webhooks endpoint object:

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    webhooks = client.Webhooks.get_all_webhooks()
    print(webhooks)
```

---

::: pyrevolut.api.webhooks.endpoint.EndpointWebhooksSync

---
