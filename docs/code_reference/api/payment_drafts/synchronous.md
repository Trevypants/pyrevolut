# Payment Drafts Synchronous Endpoints

This `Payment Drafts` endpoint provides methods to interact with the payment drafts of the authenticated user.

Example usage of the Payment Drafts endpoint object:

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    drafts = client.PaymentDrafts.get_all_payment_drafts()
    print(drafts)
```

---

::: pyrevolut.api.payment_drafts.endpoint.EndpointPaymentDraftsSync

---
