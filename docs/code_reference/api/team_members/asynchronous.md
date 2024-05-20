# Team Members Asynchronous Endpoints

This `Team Members` endpoint provides asynchronous methods to interact with the team members of the authenticated user.

Example usage of the Team Members endpoint object:

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
        members = await client.TeamMembers.get_team_members()
        print(members)

asyncio.run(run())
```

---

::: pyrevolut.api.team_members.endpoint.EndpointTeamMembersAsync

---
