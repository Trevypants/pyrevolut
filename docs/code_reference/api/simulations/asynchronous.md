# Simulations Asynchronous Endpoints

This `Simulations` endpoint provides asynchronous methods to interact with the simulations of the authenticated user.

Example usage of the Simulations endpoint object:

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
        response = await client.Simulations.simulate_account_topup(
            account_id="SOME_ACCOUNT_ID",
            amount=100.0,
            currency="USD",
            reference="Sugar Daddy :heart:",
            state=EnumTransactionState.COMPLETED,
        )
        print(response)

asyncio.run(run())
```

---

::: pyrevolut.api.simulations.endpoint.EndpointSimulationsAsync

---
