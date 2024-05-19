from uuid import UUID
from datetime import datetime

from pyrevolut.api.common import BaseEndpointSync, EnumProfileType
from pyrevolut.utils import DateTime

from pyrevolut.api.counterparties.get import (
    RetrieveListOfCounterparties,
    RetrieveCounterparty,
)
from pyrevolut.api.counterparties.post import CreateCounterparty, ValidateAccountName
from pyrevolut.api.counterparties.delete import DeleteCounterparty


class EndpointCounterpartiesSync(BaseEndpointSync):
    """The Counterparties API

    Manage counterparties that you intend to transact with.

    Request and response examples can vary based on the account provider's
    location and type of the counterparty.

    In the Sandbox environment, you cannot add real people and businesses as Revolut counterparties.
    Therefore, to help you simulate Create a counterparty requests, we have created some
    test accounts for counterparties of profile type personal.

    To add a counterparty via Revtag, use one of these pairs for the name and revtag fields respectively:

    Test User 1 & john1pvki
    Test User 2 & john2pvki
    ...
    Test User 9 & john9pvki
    """

    def get_all_counterparties(
        self,
        name: str | None = None,
        account_no: str | None = None,
        sort_code: str | None = None,
        iban: str | None = None,
        bic: str | None = None,
        created_before: datetime | DateTime | str | int | float | None = None,
        limit: int | None = None,
        **kwargs,
    ) -> list[dict] | list[RetrieveListOfCounterparties.Response]:
        """
        Get all the counterparties that you have created, or use the query parameters to filter the results.

        The counterparties are sorted by the created_at date in reverse chronological order.

        The returned counterparties are paginated. The maximum number of counterparties returned per page
        is specified by the limit parameter. To get to the next page, make a new request and use the
        created_at date of the last counterparty returned in the previous response.

        Parameters
        ----------
        name : str | None
            The name of the counterparty to retrieve. It does not need to be an exact match,
            partial match is also supported.
        account_no : str | None
            The exact account number of the counterparty to retrieve.
        sort_code : str | None
            The exact sort code of the counterparty to retrieve.
            Only allowed in combination with the account_no parameter.
        iban : str | None
            The exact IBAN of the counterparty to retrieve.
        bic : str | None
            The exact BIC of the counterparty to retrieve. Only allowed in combination with the iban parameter.
        created_before : datetime | DateTime | str | int | float | None
            Retrieves counterparties with created_at < created_before.
            The default value is the current date and time at which you are calling the endpoint.
            Provided in ISO 8601 format.
        limit : int | None
            The maximum number of counterparties returned per page.
            To get to the next page, make a new request and use the
            created_at date of the last card returned in the previous
            response as the value for created_before.

        Returns
        -------
        list[dict] | list[RetrieveListOfCounterparties.Response]
            The list of all counterparties that you have created.
        """
        endpoint = RetrieveListOfCounterparties
        path = endpoint.ROUTE
        params = endpoint.Params(
            name=name,
            account_no=account_no,
            sort_code=sort_code,
            iban=iban,
            bic=bic,
            created_before=created_before,
            limit=limit,
        )

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def get_counterparty(
        self,
        counterparty_id: UUID,
        **kwargs,
    ) -> dict | RetrieveCounterparty.Response:
        """Get the information about a specific counterparty by ID.

        Parameters
        ----------
        counterparty_id : UUID
            The ID of the counterparty to retrieve.

        Returns
        -------
        dict | RetrieveCounterparty.Response
            The information about the counterparty.
        """
        endpoint = RetrieveCounterparty
        path = endpoint.ROUTE.format(counterparty_id=counterparty_id)
        params = endpoint.Params()

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def create_counterparty(
        self,
        company_name: str | None = None,
        profile_type: EnumProfileType | None = None,
        name: str | None = None,
        individual_first_name: str | None = None,
        individual_last_name: str | None = None,
        bank_country: str | None = None,
        currency: str | None = None,
        revtag: str | None = None,
        account_no: str | None = None,
        iban: str | None = None,
        sort_code: str | None = None,
        routing_number: str | None = None,
        bic: str | None = None,
        clabe: str | None = None,
        isfc: str | None = None,
        bsb_code: str | None = None,
        address_street_line1: str | None = None,
        address_street_line2: str | None = None,
        address_region: str | None = None,
        address_city: str | None = None,
        address_country: str | None = None,
        address_postcode: str | None = None,
        **kwargs,
    ) -> dict | CreateCounterparty.Response:
        """
        Create a new counterparty to transact with.

        In the Sandbox environment, you cannot add real people and businesses as Revolut counterparties.
        To help you simulate Create a counterparty requests for counterparties of profile type personal,
        we created some test accounts. Look inside for test Revtags.

        To add a counterparty via Revtag, use one of these pairs for the name and revtag fields respectively:

            Test User 1 & john1pvki
            Test User 2 & john2pvki
            ...
            Test User 9 & john9pvki

        Parameters
        ----------
        company_name : str | None
            The name of the company counterparty.
            Use when individual_name or name isn't specified and profile_type is business.
        profile_type : EnumProfileType | None
            The type of the Revolut profile. Used when adding an existing Revolut user via Revtag.
        name : str | None
            The name of the counterparty that you create for an existing Revolut user via Revtag.
            Provide the value only when you specify personal for profile_type.
        individual_first_name : str | None
            The first name of the individual counterparty.
            Use when company_name isn't specified.
        individual_last_name : str | None
            The last name of the individual counterparty.
            Use when company_name isn't specified.
        bank_country : str | None
            The country of the counterparty's bank as the 2-letter ISO 3166 code.
        currency : str | None
            ISO 4217 currency code in upper case.
        revtag : str | None
            The Revtag of the counterparty to add.
        account_no : str | None
            The bank account number of the counterparty.
        iban : str | None
            The IBAN number of the counterparty's account. This field is displayed for IBAN countries.
        sort_code : str | None
            The sort code of the counterparty's bank. This field is displayed for GBP accounts.
        routing_number : str | None
            The routing number of the counterparty's bank. This field is displayed for USD accounts.
        bic : str | None
            The BIC number of the counterparty's account. This field is required for non-SEPA IBAN/SWIFT.
        clabe : str | None
            The CLABE number of the counterparty's account. This field is required for SWIFT MX.
        isfc : str | None
            The ISFC number of the counterparty's account. This field is required for INR accounts.
        bsb_code : str | None
            The BSB code of the counterparty's account. This field is required for AUD accounts.
        address_street_line1 : str | None
            Street line 1 information.
        address_street_line2 : str | None
            Street line 2 information.
        address_region : str | None
            The name of the region.
        address_city : str | None
            The name of the city.
        address_country : str | None
            The country of the counterparty's address as the 2-letter ISO 3166 code.
        address_postcode : str | None
            The postcode of the counterparty's address.

        Returns
        -------
        dict | CreateCounterparty.Response
            A dict with the information about the created counterparty.
        """
        endpoint = CreateCounterparty
        path = endpoint.ROUTE
        body = endpoint.Body(
            company_name=company_name,
            profile_type=profile_type,
            name=name,
            individual_name=(
                endpoint.Body.ModelIndividualName(
                    first_name=individual_first_name,
                    last_name=individual_last_name,
                )
                if individual_first_name is not None or individual_last_name is not None
                else None
            ),
            bank_country=bank_country,
            currency=currency,
            revtag=revtag,
            account_no=account_no,
            iban=iban,
            sort_code=sort_code,
            routing_number=routing_number,
            bic=bic,
            clabe=clabe,
            isfc=isfc,
            bsb_code=bsb_code,
            address=(
                endpoint.Body.ModelAddress(
                    street_line1=address_street_line1,
                    street_line2=address_street_line2,
                    region=address_region,
                    city=address_city,
                    country=address_country,
                    postcode=address_postcode,
                )
                if address_country is not None and address_postcode is not None
                else None
            ),
        )

        return self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def validate_account_name(
        self,
        account_no: str,
        sort_code: str,
        company_name: str | None = None,
        individual_first_name: str | None = None,
        individual_last_name: str | None = None,
        **kwargs,
    ) -> dict | ValidateAccountName.Response:
        """
        Use Confirmation of Payee (CoP) to validate a UK counterparty's account name
        against their account number and sort code when adding a counterparty or making a
        transfer to a new or existing counterparty.

        Note
        ----
        Confirmation of Payee is an account name checking system in the UK that helps clients
        to make sure payments aren't sent to the wrong bank or building society account.

        When performing the check, you must specify the account type by providing the name for either
        an individual (personal account) or a company (business account).

        Caution
        -------
        The CoP check does not protect you against all kinds of fraud. It only checks if the name you provided for an account matches that account's details.
        Even if the counterparty's details match, you should still exercise due caution when transferring funds.

        This functionality is only available to UK-based businesses.

        Parameters
        ----------
        account_no : str
            The account number of the counterparty.
        sort_code : str
            The sort code of the counterparty's account.
        company_name : str | None
            The name of the business counterparty. Use when individual_name is not specified.
        individual_first_name : str | None
            The first name of the individual counterparty.
            Use when company_name isn't specified.
        individual_last_name : str | None
            The last name of the individual counterparty.
            Use when company_name isn't specified.

        Returns
        -------
        dict | ValidateAccountName.Response
            A dict with the information about the validated account name.
        """
        endpoint = ValidateAccountName
        path = endpoint.ROUTE
        body = endpoint.Body(
            account_no=account_no,
            sort_code=sort_code,
            company_name=company_name,
            individual_name=(
                endpoint.Body.ModelIndividualName(
                    first_name=individual_first_name,
                    last_name=individual_last_name,
                )
                if individual_first_name is not None or individual_last_name is not None
                else None
            ),
        )

        return self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def delete_counterparty(
        self,
        counterparty_id: UUID,
        **kwargs,
    ) -> dict | DeleteCounterparty.Response:
        """Delete a counterparty with the given ID.
        When a counterparty is deleted, you cannot make any payments to the counterparty.

        Parameters
        ----------
        counterparty_id : UUID
            The ID of the counterparty to delete.

        Returns
        -------
        dict | DeleteCounterparty.Response
            An empty dict.
        """
        endpoint = DeleteCounterparty
        path = endpoint.ROUTE.format(counterparty_id=counterparty_id)
        params = endpoint.Params()

        return self.client.delete(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )
