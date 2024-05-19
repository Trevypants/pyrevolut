import time
import asyncio
import pytest
import random

from pyrevolut.client import Client


def test_sync_get_team_members(sync_client: Client):
    """Test the sync `get_team_members` team members method"""

    with pytest.raises(ValueError, match="This feature is not available in Sandbox."):
        # Get all team members (no params)
        team_members = sync_client.TeamMembers.get_team_members()
        time.sleep(random.randint(1, 3))

        assert isinstance(team_members, list)
        assert all(isinstance(team_member, dict) for team_member in team_members)

        # Get all team members (with params)
        team_members = sync_client.TeamMembers.get_team_members(
            created_before="2020-01-01",
            limit=10,
        )
        time.sleep(random.randint(1, 3))
        assert isinstance(team_members, list)
        assert len(team_members) == 0


def test_sync_get_team_roles(sync_client: Client):
    """Test the sync `get_team_roles` team members method"""

    with pytest.raises(ValueError, match="This feature is not available in Sandbox."):
        # Get all team roles (no params)
        team_roles = sync_client.TeamMembers.get_team_roles()
        time.sleep(random.randint(1, 3))

        assert isinstance(team_roles, list)
        assert all(isinstance(team_role, dict) for team_role in team_roles)

        # Get all team roles (with params)
        team_roles = sync_client.TeamMembers.get_team_roles(
            created_before="2020-01-01",
            limit=10,
        )
        time.sleep(random.randint(1, 3))
        assert isinstance(team_roles, list)
        assert len(team_roles) == 0


def test_sync_invite_team_member(sync_client: Client):
    """Test the sync `invite_team_member` team members method"""

    with pytest.raises(ValueError, match="This feature is not available in Sandbox."):
        # Get all team roles
        team_roles = sync_client.TeamMembers.get_team_roles()
        time.sleep(random.randint(1, 3))

        # Get the first team role
        team_role = team_roles[0]

        # Invite a new team member
        response = sync_client.TeamMembers.invite_team_member(
            email="johndoe@example.com",
            role_id=team_role["id"],
        )
        time.sleep(random.randint(1, 3))
        assert isinstance(response, dict)
        assert response["email"] == "johndoe@example.com"


@pytest.mark.asyncio
async def test_async_get_team_members(async_client: Client):
    """Test the async `get_team_members` team members method"""

    with pytest.raises(ValueError, match="This feature is not available in Sandbox."):
        # Get all team members (no params)
        team_members = await async_client.TeamMembers.get_team_members()
        await asyncio.sleep(random.randint(1, 3))

        assert isinstance(team_members, list)
        assert all(isinstance(team_member, dict) for team_member in team_members)

        # Get all team members (with params)
        team_members = await async_client.TeamMembers.get_team_members(
            created_before="2020-01-01",
            limit=10,
        )
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(team_members, list)
        assert len(team_members) == 0


@pytest.mark.asyncio
async def test_async_get_team_roles(async_client: Client):
    """Test the async `get_team_roles` team members method"""

    with pytest.raises(ValueError, match="This feature is not available in Sandbox."):
        # Get all team roles (no params)
        team_roles = await async_client.TeamMembers.get_team_roles()
        await asyncio.sleep(random.randint(1, 3))

        assert isinstance(team_roles, list)
        assert all(isinstance(team_role, dict) for team_role in team_roles)

        # Get all team roles (with params)
        team_roles = await async_client.TeamMembers.get_team_roles(
            created_before="2020-01-01",
            limit=10,
        )
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(team_roles, list)
        assert len(team_roles) == 0


@pytest.mark.asyncio
async def test_async_invite_team_member(async_client: Client):
    """Test the async `invite_team_member` team members method"""

    with pytest.raises(ValueError, match="This feature is not available in Sandbox."):
        # Get all team roles
        team_roles = await async_client.TeamMembers.get_team_roles()
        await asyncio.sleep(random.randint(1, 3))

        # Get the first team role
        team_role = team_roles[0]

        # Invite a new team member
        response = await async_client.TeamMembers.invite_team_member(
            email="johndoe@example.com",
            role_id=team_role["id"],
        )
        await asyncio.sleep(random.randint(1, 3))
        assert isinstance(response, dict)
        assert response["email"] == "johndoe@example.com"
