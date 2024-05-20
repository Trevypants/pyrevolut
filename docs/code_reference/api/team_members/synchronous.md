# Team Members Synchronous Endpoints

This `Team Members` endpoint provides methods to interact with the team members of the authenticated user.

Example usage of the Team Members endpoint object:

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

with client:
    members = client.TeamMembers.get_team_members()
    print(members)
```

---

::: pyrevolut.api.team_members.endpoint.EndpointTeamMembersSync

---
