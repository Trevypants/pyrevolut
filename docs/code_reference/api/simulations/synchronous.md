# Simulations Synchronous Endpoints

This `Simulations` endpoint provides methods to interact with the simulations of the authenticated user.

Example usage of the Simulations endpoint object:

```python
from pyrevolut.client import Client
from pyrevolut.api import EnumTransactionState

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    response = client.Simulations.simulate_account_topup(
        account_id="SOME_ACCOUNT_ID",
        amount=100.0,
        currency="USD",
        reference="Sugar Daddy :heart:",
        state=EnumTransactionState.COMPLETED,
    )
    print(response)
```

---

::: pyrevolut.api.simulations.endpoint.EndpointSimulationsSync

---
