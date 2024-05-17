from uuid import UUID
from datetime import datetime

from pyrevolut.utils.datetime import DateTime
from pyrevolut.api.common import BaseEndpoint

from .get import RetrieveListOfTeamMembers, RetrieveTeamRoles
from .post import InviteTeamMember


class EndpointTeamMembers(BaseEndpoint):
    """The Team Members API

    Retrieve information on existing team members of your organisation and invite new members.

    This feature is available in the UK, US and the EEA.

    This feature is not available in Sandbox.
    """

    def get_team_members(
        self,
        created_before: datetime | DateTime | str | int | float | None = None,
        limit: int | None = None,
        **kwargs,
    ):
        """
        Get information about all the team members of your business.

        The results are paginated and sorted by the created_at date in reverse chronological order.

        Note
        ----
        This feature is available in the UK, US and the EEA.

        This feature is not available in Sandbox.

        Parameters
        ----------
        created_before : datetime | DateTime | str | int | float | None
            Retrieves team members with created_at < created_before.
            The default value is the current date and time at which you are calling the endpoint.
            Provided in ISO 8601 format.
        limit : int | None
            The maximum number of team members returned per page.
            To get to the next page, make a new request and use the
            created_at date of the last team member returned in the previous
            response as the value for created_before.

            If not provided, the default value is 100.

        Returns
        -------
        list
            The list of all team members in your organisation.
        """
        endpoint = RetrieveListOfTeamMembers
        path = endpoint.ROUTE
        params = endpoint.Params(
            created_before=created_before,
            limit=limit,
        )

        response = self.client.get(
            path=path,
            params=params,
            **kwargs,
        )

        return [endpoint.Response(**resp).model_dump() for resp in response.json()]

    def get_team_roles(
        self,
        created_before: datetime | DateTime | str | int | float | None = None,
        limit: int | None = None,
        **kwargs,
    ):
        """
        Get the list of roles for your business.

        The results are paginated and sorted by the created_at date in reverse chronological order.

        This feature is available in the UK, US and the EEA.

        This feature is not available in Sandbox.

        Parameters
        ----------
        created_before : datetime | DateTime | str | int | float | None
            Retrieves team roles with created_at < created_before.
            The default value is the current date and time at which you are calling the endpoint.
            Provided in ISO 8601 format.
        limit : int | None
            The maximum number of team roles returned per page.
            To get to the next page, make a new request and use the
            created_at date of the last role returned in the previous
            response as the value for created_before.

            If not provided, the default value is 100.

        Returns
        -------
        list
            The list of all team roles in your organisation.
        """
        endpoint = RetrieveTeamRoles
        path = endpoint.ROUTE
        params = endpoint.Params(
            created_before=created_before,
            limit=limit,
        )

        response = self.client.get(
            path=path,
            params=params,
            **kwargs,
        )

        return [endpoint.Response(**resp).model_dump() for resp in response.json()]

    def invite_team_member(
        self,
        email: str,
        role_id: UUID | str,
        **kwargs,
    ):
        """
        Invite a new member to your business account.

        When you invite a new team member to your business account,
        an invitation is sent to their email address that you provided in this request.
        To join your business account, the new team member has to accept this invitation.

        Note
        ----
        This feature is available in the UK, US and the EEA.

        This feature is not available in Sandbox.

        Parameters
        ----------
        email : str
            The email address of the invited member.
        role_id : UUID | str
            The ID of the role to assign to the new member.

        Returns
        -------
        dict
            The response model.
        """
        endpoint = InviteTeamMember
        path = endpoint.ROUTE
        body = endpoint.Body(
            email=email,
            role_id=role_id,
        )

        response = self.client.post(
            path=path,
            body=body,
            **kwargs,
        )

        return endpoint.Response(**response.json()).model_dump()

    async def aget_team_members(
        self,
        created_before: datetime | DateTime | str | int | float | None = None,
        limit: int | None = None,
        **kwargs,
    ):
        """
        Get information about all the team members of your business.

        The results are paginated and sorted by the created_at date in reverse chronological order.

        Note
        ----
        This feature is available in the UK, US and the EEA.

        This feature is not available in Sandbox.

        Parameters
        ----------
        created_before : datetime | DateTime | str | int | float | None
            Retrieves team members with created_at < created_before.
            The default value is the current date and time at which you are calling the endpoint.
            Provided in ISO 8601 format.
        limit : int | None
            The maximum number of team members returned per page.
            To get to the next page, make a new request and use the
            created_at date of the last team member returned in the previous
            response as the value for created_before.

            If not provided, the default value is 100.

        Returns
        -------
        list
            The list of all team members in your organisation.
        """
        endpoint = RetrieveListOfTeamMembers
        path = endpoint.ROUTE
        params = endpoint.Params(
            created_before=created_before,
            limit=limit,
        )

        response = await self.client.aget(
            path=path,
            params=params,
            **kwargs,
        )

        return [endpoint.Response(**resp).model_dump() for resp in response.json()]

    async def aget_team_roles(
        self,
        created_before: datetime | DateTime | str | int | float | None = None,
        limit: int | None = None,
        **kwargs,
    ):
        """
        Get the list of roles for your business.

        The results are paginated and sorted by the created_at date in reverse chronological order.

        This feature is available in the UK, US and the EEA.

        This feature is not available in Sandbox.

        Parameters
        ----------
        created_before : datetime | DateTime | str | int | float | None
            Retrieves team roles with created_at < created_before.
            The default value is the current date and time at which you are calling the endpoint.
            Provided in ISO 8601 format.
        limit : int | None
            The maximum number of team roles returned per page.
            To get to the next page, make a new request and use the
            created_at date of the last role returned in the previous
            response as the value for created_before.

            If not provided, the default value is 100.

        Returns
        -------
        list
            The list of all team roles in your organisation.
        """
        endpoint = RetrieveTeamRoles
        path = endpoint.ROUTE
        params = endpoint.Params(
            created_before=created_before,
            limit=limit,
        )

        response = await self.client.aget(
            path=path,
            params=params,
            **kwargs,
        )

        return [endpoint.Response(**resp).model_dump() for resp in response.json()]

    async def ainvite_team_member(
        self,
        email: str,
        role_id: UUID | str,
        **kwargs,
    ):
        """
        Invite a new member to your business account.

        When you invite a new team member to your business account,
        an invitation is sent to their email address that you provided in this request.
        To join your business account, the new team member has to accept this invitation.

        Note
        ----
        This feature is available in the UK, US and the EEA.

        This feature is not available in Sandbox.

        Parameters
        ----------
        email : str
            The email address of the invited member.
        role_id : UUID | str
            The ID of the role to assign to the new member.

        Returns
        -------
        dict
            The response model.
        """
        endpoint = InviteTeamMember
        path = endpoint.ROUTE
        body = endpoint.Body(
            email=email,
            role_id=role_id,
        )

        response = await self.client.apost(
            path=path,
            body=body,
            **kwargs,
        )

        return endpoint.Response(**response.json()).model_dump()
