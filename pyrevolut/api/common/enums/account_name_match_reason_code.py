from enum import StrEnum


class EnumAccountNameMatchReasonCode(StrEnum):
    """Account Name Match Reason Code Enum

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
    """

    CLOSE_MATCH = "close_match"
    INDIVIDUAL_ACCOUNT_NAME_MATCHED = "individual_account_name_matched"
    COMPANY_ACCOUNT_NAME_MATCHED = "company_account_name_matched"
    INDIVIDUAL_ACCOUNT_CLOSE_MATCH = "individual_account_close_match"
    COMPANY_ACCOUNT_CLOSE_MATCH = "company_account_close_match"
    NOT_MATCHED = "not_matched"
    ACCOUNT_DOES_NOT_EXIST = "account_does_not_exist"
    ACCOUNT_SWITCHED = "account_switched"
    CANNOT_BE_CHECKED = "cannot_be_checked"
