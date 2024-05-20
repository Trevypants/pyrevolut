# Payout Links Synchronous Endpoints

This `Payout Links` endpoint provides methods to interact with the payout links of the authenticated user.

Example usage of the Payout links endpoint object:

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    links = client.PayoutLinks.get_all_payout_links()
    print(links)
```

---

::: pyrevolut.api.payout_links.endpoint.EndpointPayoutLinksSync

---
