from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from pyrevolut.api.common import (
    EnumAccountNameMatchCode,
    EnumAccountNameMatchReasonType,
    EnumAccountNameMatchReasonCode,
)


class ValidateAccountName:
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
    """

    ROUTE = "/1.0/account-name-validation"

    class Body(BaseModel):
        """
        Request body for the endpoint.
        """

        class ModelIndividualName(BaseModel):
            """The name of the individual counterparty. Use when company_name isn't specified."""

            first_name: Annotated[
                str | None,
                Field(description="The first name of the individual counterparty."),
            ] = None
            last_name: Annotated[
                str | None,
                Field(description="The last name of the individual counterparty."),
            ] = None

        account_no: Annotated[
            str,
            Field(
                description="The account number of the counterparty.",
            ),
        ]
        sort_code: Annotated[
            str,
            Field(
                description="The sort code of the counterparty's account.",
            ),
        ]
        company_name: Annotated[
            str | None,
            Field(
                description="The name of the business counterparty. Use when individual_name is not specified.",
            ),
        ] = None
        individual_name: Annotated[
            ModelIndividualName | None,
            Field(
                description="The name of the individual counterparty. Use when company_name is not specified.",
            ),
        ] = None

        @model_validator(mode="after")
        def check_inputs(self) -> "ValidateAccountName.Body":
            """
            Ensure that either the individual_name or company_name is provided.
            """
            if not self.company_name and not self.individual_name:
                raise ValueError(
                    "You must provide either the company_name or individual_name."
                )
            if self.company_name and self.individual_name:
                raise ValueError(
                    "You must provide either the company_name or individual_name, not both."
                )
            return self

    class Response(BaseModel):
        """
        Response model for the endpoint.
        """

        class ModelIndividualName(BaseModel):
            """The name of the individual counterparty. Use when company_name isn't specified."""

            first_name: Annotated[
                str | None,
                Field(description="The first name of the individual counterparty."),
            ] = None
            last_name: Annotated[
                str | None,
                Field(description="The last name of the individual counterparty."),
            ] = None

        class ModelReason(BaseModel):
            """
            A code which explains why a given result was returned.
            For example, it might happen that the details you provided match the account details,
            but you specified the counterparty as an individual, and the account type is business.
            """

            type: Annotated[
                EnumAccountNameMatchReasonType | None,
                Field(
                    description="""
                    The reason type. Possible values:

                        uk_cop:
                            The CoP reason
                    """,
                ),
            ] = None
            code: Annotated[
                EnumAccountNameMatchReasonCode | None,
                Field(
                    description="""
                    The reason code. Possible values:

                        close_match:
                            The provided name is similar to the account name, the account type is correct.
                            The actual name is returned.
                        individual_account_name_matched:
                            The names match but the counterparty is an individual, not a business.
                        company_account_name_matched:
                            The names match but the counterparty is a business, not an individual.
                        individual_account_close_match:
                            The provided name is similar to the account name, and the account type is incorrect
                            - the counterparty is an individual, not a business. The actual name is returned.
                        company_account_close_match:
                            The provided name is similar to the account name, and the account type is incorrect
                            - the counterparty is a business, not an individual. The actual name is returned.
                        not_matched:
                            The account details don't match the provided values.
                        account_does_not_exist:
                            The account does not exist.
                        account_switched:
                            The account has been switched using the Current Account Switching Service.
                            Please contact the recipient for updated account details.
                        cannot_be_checked:
                            The account cannot be checked.
                    """,
                ),
            ] = None

        result_code: Annotated[
            EnumAccountNameMatchCode,
            Field(
                description="""
                The result of the account name check. Possible values:

                    matched:
                        The name and account type match the provided values.
                    close_match:
                        The name and account type are similar to the provided values.
                        The actual values are returned.
                    not_matched:
                        The name and account type don't match the provided values.
                    cannot_be_checked:
                        The check cannot be performed and retries won't help.
                        For example, the recipient's bank doesn't support CoP.
                    temporarily_unavailable:
                        The check cannot be performed right now.
                        For example, the recipient's bank didn't respond to our request.
                        You should retry the request later.
                """
            ),
        ]
        reason: Annotated[
            ModelReason | None,
            Field(
                description="""
                A code which explains why a given result was returned.
                For example, it might happen that the details you provided match the account details,
                but you specified the counterparty as an individual, and the account type is business.
                """,
            ),
        ] = None
        company_name: Annotated[
            str | None,
            Field(
                description="The name of the business counterparty. Use when individual_name is not specified.",
            ),
        ] = None
        individual_name: Annotated[
            ModelIndividualName | None,
            Field(
                description="The name of the individual counterparty. Use when company_name is not specified.",
            ),
        ] = None
