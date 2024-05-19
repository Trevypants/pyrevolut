from typing import Literal, Type
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel

from pyrevolut.utils import DateTime
from pyrevolut.exceptions import InvalidEnvironmentException
from pyrevolut.api.common import BaseEndpointSync, EnumMerchantCategory
from pyrevolut.api.cards.get import (
    RetrieveListOfCards,
    RetrieveCardDetails,
    RetrieveSensitiveCardDetails,
)
from pyrevolut.api.cards.post import CreateCard, FreezeCard, UnfreezeCard
from pyrevolut.api.cards.patch import UpdateCardDetails
from pyrevolut.api.cards.delete import TerminateCard


class EndpointCardsSync(BaseEndpointSync):
    """The Cards API
    Manage cards for the business team members, freeze, unfreeze,
    terminate and update card settings, such as transaction limits.

    This feature is available in the UK, US and the EEA.
    This feature is not available in Sandbox.
    """

    def get_all_cards(
        self,
        created_before: datetime | DateTime | str | int | float | None = None,
        limit: int | None = None,
        **kwargs,
    ) -> list[dict] | list[RetrieveListOfCards.Response]:
        """
        Get the list of all cards in your organisation.
        The results are paginated and sorted by the created_at date in reverse chronological order.

        Parameters
        ----------
        created_before : datetime | DateTime | str | int | float | None
            Retrieves cards with created_at < created_before.
            The default value is the current date and time at which you are calling the endpoint.
            Provided in ISO 8601 format.
        limit : int | None
            The maximum number of cards returned per page.
            To get to the next page, make a new request and use the
            created_at date of the last card returned in the previous
            response as the value for created_before.

            If not provided, the default value is 100.

        Returns
        -------
        list[dict] | list[RetrieveListOfCards.Response]
            The list of all cards in your organisation.
        """
        self.__check_sandbox()
        endpoint = RetrieveListOfCards
        path = endpoint.ROUTE
        params = endpoint.Params(
            created_before=created_before,
            limit=limit,
        )

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def get_card(
        self,
        card_id: UUID,
        **kwargs,
    ) -> dict | RetrieveCardDetails.Response:
        """
        Get the details of a specific card, based on its ID.

        Parameters
        ----------
        card_id : UUID
            The card ID.

        Returns
        -------
        dict | RetrieveCardDetails.Response
            The details of the card.
        """
        self.__check_sandbox()
        endpoint = RetrieveCardDetails
        path = endpoint.ROUTE.format(card_id=card_id)
        params = endpoint.Params()

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def get_card_sensitive_details(
        self,
        card_id: UUID,
        **kwargs,
    ) -> dict | RetrieveSensitiveCardDetails.Response:
        """
        Get sensitive details of a specific card, based on its ID.
        Requires the READ_SENSITIVE_CARD_DATA token scope.

        Parameters
        ----------
        card_id : UUID
            The card ID.

        Returns
        -------
        dict | RetrieveSensitiveCardDetails.Response
            The sensitive details of the card.
        """
        self.__check_sandbox()
        endpoint = RetrieveSensitiveCardDetails
        path = endpoint.ROUTE.format(card_id=card_id)
        params = endpoint.Params()

        return self.client.get(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def create_card(
        self,
        request_id: str,
        holder_id: UUID,
        label: str | None = None,
        accounts: list[UUID] | None = None,
        categories: list[EnumMerchantCategory] | None = None,
        single_limit_amount: Decimal | None = None,
        single_limit_currency: str | None = None,
        day_limit_amount: Decimal | None = None,
        day_limit_currency: str | None = None,
        week_limit_amount: Decimal | None = None,
        week_limit_currency: str | None = None,
        month_limit_amount: Decimal | None = None,
        month_limit_currency: str | None = None,
        quarter_limit_amount: Decimal | None = None,
        quarter_limit_currency: str | None = None,
        year_limit_amount: Decimal | None = None,
        year_limit_currency: str | None = None,
        all_time_limit_amount: Decimal | None = None,
        all_time_limit_currency: str | None = None,
        **kwargs,
    ) -> dict | CreateCard.Response:
        """
        Create a new card for an existing member of your Revolut Business team.

        When using the API, you can create only virtual cards.
        To create a physical card, use the Revolut Business app.

        Parameters
        ----------
        request_id : str
            A unique ID of the request that you provide.
            This ID is used to prevent duplicate card creation requests in case
            of a lost connection or client error, so make sure you use the same
            request_id for requests related to the same card.
            The deduplication is limited to 24 hours counting from the first request
            using a given ID.
        holder_id : UUID
            The ID of the team member who will be the holder of the card.
        label : str | None
            The label for the issued card, displayed in the UI to help distinguish between cards.
            If not specified, no label will be added.
        accounts : list[UUID] | None
            The list of accounts to link to the card. If not specified, all accounts will be linked.
        categories : list[EnumMerchantCategory] | None
            The list of merchant categories to link to the card. If not specified, all categories will be linked.
        single_limit_amount : Decimal | None
            The maximum amount for a single transaction.
        single_limit_currency : str | None
            The currency of the single transaction limit.
        day_limit_amount : Decimal | None
            The maximum amount for transactions in a day.
        day_limit_currency : str | None
            The currency of the day limit.
        week_limit_amount : Decimal | None
            The maximum amount for transactions in a week.
        week_limit_currency : str | None
            The currency of the week limit.
        month_limit_amount : Decimal | None
            The maximum amount for transactions in a month.
        month_limit_currency : str | None
            The currency of the month limit.
        quarter_limit_amount : Decimal | None
            The maximum amount for transactions in a quarter.
        quarter_limit_currency : str | None
            The currency of the quarter limit.
        year_limit_amount : Decimal | None
            The maximum amount for transactions in a year.
        year_limit_currency : str | None
            The currency of the year limit.
        all_time_limit_amount : Decimal | None
            The maximum amount for transactions in the card's lifetime.
        all_time_limit_currency : str | None
            The currency of the all-time limit.

        Returns
        -------
        dict | CreateCard.Response
            The details of the created card.
        """
        self.__check_sandbox()
        endpoint = CreateCard
        path = endpoint.ROUTE

        # Create the SpendingLimits model (if applicable)
        spending_limits = endpoint.Body.ModelSpendingLimits(
            single=(
                endpoint.Body.ModelSpendingLimits.ModelSingle(
                    amount=single_limit_amount,
                    currency=single_limit_currency,
                )
                if single_limit_amount is not None and single_limit_currency is not None
                else None
            ),
            day=(
                endpoint.Body.ModelSpendingLimits.ModelDay(
                    amount=day_limit_amount,
                    currency=day_limit_currency,
                )
                if day_limit_amount is not None and day_limit_currency is not None
                else None
            ),
            week=(
                endpoint.Body.ModelSpendingLimits.ModelWeek(
                    amount=week_limit_amount,
                    currency=week_limit_currency,
                )
                if week_limit_amount is not None and week_limit_currency is not None
                else None
            ),
            month=(
                endpoint.Body.ModelSpendingLimits.ModelMonth(
                    amount=month_limit_amount,
                    currency=month_limit_currency,
                )
                if month_limit_amount is not None and month_limit_currency is not None
                else None
            ),
            quarter=(
                endpoint.Body.ModelSpendingLimits.ModelQuarter(
                    amount=quarter_limit_amount,
                    currency=quarter_limit_currency,
                )
                if quarter_limit_amount is not None
                and quarter_limit_currency is not None
                else None
            ),
            year=(
                endpoint.Body.ModelSpendingLimits.ModelYear(
                    amount=year_limit_amount,
                    currency=year_limit_currency,
                )
                if year_limit_amount is not None and year_limit_currency is not None
                else None
            ),
            all_time=(
                endpoint.Body.ModelSpendingLimits.ModelAllTime(
                    amount=all_time_limit_amount,
                    currency=all_time_limit_currency,
                )
                if all_time_limit_amount is not None
                and all_time_limit_currency is not None
                else None
            ),
        )
        if not any(
            [
                spending_limits.single is not None,
                spending_limits.day is not None,
                spending_limits.week is not None,
                spending_limits.month is not None,
                spending_limits.quarter is not None,
                spending_limits.year is not None,
                spending_limits.all_time is not None,
            ]
        ):
            spending_limits = None

        body = endpoint.Body(
            request_id=request_id,
            virtual=True,
            holder_id=holder_id,
            label=label,
            accounts=accounts,
            categories=categories,
            spending_limits=spending_limits,
        )

        return self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def freeze_card(
        self,
        card_id: UUID,
        **kwargs,
    ) -> dict | FreezeCard.Response:
        """
        Freeze a card to make it temporarily unavailable for spending.
        You can only freeze a card that is in the state active.

        A successful freeze changes the card's state to frozen,
        and no content is returned in the response.

        Parameters
        ----------
        card_id : UUID
            The card ID.

        Returns
        -------
        dict | FreezeCard.Response
            An empty dictionary.
        """
        self.__check_sandbox()
        endpoint = FreezeCard
        path = endpoint.ROUTE.format(card_id=card_id)
        body = endpoint.Body()

        return self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def unfreeze_card(
        self,
        card_id: UUID,
        **kwargs,
    ) -> dict | UnfreezeCard.Response:
        """
        Unfreeze a card to make it available for spending again.
        You can only unfreeze a card that is in the state frozen.

        A successful unfreeze changes the card's state to active,
        and no content is returned in the response.

        Parameters
        ----------
        card_id : UUID
            The card ID.

        Returns
        -------
        dict | UnfreezeCard.Response
            An empty dictionary.
        """
        self.__check_sandbox()
        endpoint = UnfreezeCard
        path = endpoint.ROUTE.format(card_id=card_id)
        body = endpoint.Body()

        self.client.post(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def update_card(
        self,
        card_id: UUID,
        label: str | None = None,
        categories: list[EnumMerchantCategory] | Literal["null"] | None = None,
        single_limit_amount: Decimal | Literal["null"] | None = None,
        single_limit_currency: str | Literal["null"] | None = None,
        day_limit_amount: Decimal | Literal["null"] | None = None,
        day_limit_currency: str | Literal["null"] | None = None,
        week_limit_amount: Decimal | Literal["null"] | None = None,
        week_limit_currency: str | Literal["null"] | None = None,
        month_limit_amount: Decimal | Literal["null"] | None = None,
        month_limit_currency: str | Literal["null"] | None = None,
        quarter_limit_amount: Decimal | Literal["null"] | None = None,
        quarter_limit_currency: str | Literal["null"] | None = None,
        year_limit_amount: Decimal | Literal["null"] | None = None,
        year_limit_currency: str | Literal["null"] | None = None,
        all_time_limit_amount: Decimal | Literal["null"] | None = None,
        all_time_limit_currency: str | Literal["null"] | None = None,
        **kwargs,
    ) -> dict | UpdateCardDetails.Response:
        """
        Update details of a specific card, based on its ID.
        Updating a spending limit does not reset the spending counter.

        Parameters
        ----------
        card_id : UUID
            The card ID.
        label : str | None
            The label of the card.
        categories : list[EnumMerchantCategory] | Literal["null"] | None
            The list of merchant categories to link to the card.
            If set to 'null', all categories will be linked.
        single_limit_amount : Decimal | Literal["null"] | None
            The maximum amount for a single transaction.
            If set to 'null', the limit will be removed.
        single_limit_currency : str | Literal["null"] | None
            The currency of the single transaction limit.
            If set to 'null', the limit will be removed.
        day_limit_amount : Decimal | Literal["null"] | None
            The maximum amount for transactions in a day.
            If set to 'null', the limit will be removed.
        day_limit_currency : str | Literal["null"] | None
            The currency of the day limit.
            If set to 'null', the limit will be removed.
        week_limit_amount : Decimal | Literal["null"] | None
            The maximum amount for transactions in a week.
            If set to 'null', the limit will be removed.
        week_limit_currency : str | Literal["null"] | None
            The currency of the week limit.
            If set to 'null', the limit will be removed.
        month_limit_amount : Decimal | Literal["null"] | None
            The maximum amount for transactions in a month.
            If set to 'null', the limit will be removed.
        month_limit_currency : str | Literal["null"] | None
            The currency of the month limit.
            If set to 'null', the limit will be removed.
        quarter_limit_amount : Decimal | Literal["null"] | None
            The maximum amount for transactions in a quarter.
            If set to 'null', the limit will be removed.
        quarter_limit_currency : str | Literal["null"] | None
            The currency of the quarter limit.
            If set to 'null', the limit will be removed.
        year_limit_amount : Decimal | Literal["null"] | None
            The maximum amount for transactions in a year.
            If set to 'null', the limit will be removed.
        year_limit_currency : str | Literal["null"] | None
            The currency of the year limit.
            If set to 'null', the limit will be removed.
        all_time_limit_amount : Decimal | Literal["null"] | None
            The maximum amount for transactions in the card's lifetime.
            If set to 'null', the limit will be removed.
        all_time_limit_currency : str | Literal["null"] | None
            The currency of the all-time limit.
            If set to 'null', the limit will be removed.

        Returns
        -------
        dict | UpdateCardDetails.Response
            The updated details of the card.
        """
        self.__check_sandbox()
        endpoint = UpdateCardDetails
        path = endpoint.ROUTE.format(card_id=card_id)

        # Create the SpendingLimits model (if applicable)
        spending_limits = endpoint.Body.ModelSpendingLimits(
            single=self.__process_limit_model(
                model=endpoint.Body.ModelSpendingLimits.ModelSingle,
                amount=single_limit_amount,
                currency=single_limit_currency,
            ),
            day=self.__process_limit_model(
                model=endpoint.Body.ModelSpendingLimits.ModelDay,
                amount=day_limit_amount,
                currency=day_limit_currency,
            ),
            week=self.__process_limit_model(
                model=endpoint.Body.ModelSpendingLimits.ModelWeek,
                amount=week_limit_amount,
                currency=week_limit_currency,
            ),
            month=self.__process_limit_model(
                model=endpoint.Body.ModelSpendingLimits.ModelMonth,
                amount=month_limit_amount,
                currency=month_limit_currency,
            ),
            quarter=self.__process_limit_model(
                model=endpoint.Body.ModelSpendingLimits.ModelQuarter,
                amount=quarter_limit_amount,
                currency=quarter_limit_currency,
            ),
            year=self.__process_limit_model(
                model=endpoint.Body.ModelSpendingLimits.ModelYear,
                amount=year_limit_amount,
                currency=year_limit_currency,
            ),
            all_time=self.__process_limit_model(
                model=endpoint.Body.ModelSpendingLimits.ModelAllTime,
                amount=all_time_limit_amount,
                currency=all_time_limit_currency,
            ),
        )
        if not any(
            [
                spending_limits.single is not None,
                spending_limits.day is not None,
                spending_limits.week is not None,
                spending_limits.month is not None,
                spending_limits.quarter is not None,
                spending_limits.year is not None,
                spending_limits.all_time is not None,
            ]
        ):
            spending_limits = None
        elif all(
            [
                spending_limits.single == "null",
                spending_limits.day == "null",
                spending_limits.week == "null",
                spending_limits.month == "null",
                spending_limits.quarter == "null",
                spending_limits.year == "null",
                spending_limits.all_time == "null",
            ]
        ):
            spending_limits = "null"

        body = endpoint.Body(
            label=label,
            categories=categories,
            spending_limits=spending_limits,
        )

        return self.client.patch(
            path=path,
            response_model=endpoint.Response,
            body=body,
            **kwargs,
        )

    def delete_card(
        self,
        card_id: UUID,
        **kwargs,
    ) -> dict | TerminateCard.Response:
        """
        Terminate a specific card, based on its ID.

        Once the card is terminated, it will not be returned by the API.

        A successful response does not get any content in return.

        Parameters
        ----------
        card_id : UUID
            The card ID.

        Returns
        -------
        dict | TerminateCard.Response
            An empty dictionary.
        """
        self.__check_sandbox()
        endpoint = TerminateCard
        path = endpoint.ROUTE.format(card_id=card_id)
        params = endpoint.Params()

        return self.client.delete(
            path=path,
            response_model=endpoint.Response,
            params=params,
            **kwargs,
        )

    def __process_limit_model(
        self,
        model: Type[BaseModel],
        amount: Decimal | None,
        currency: str | None,
    ):
        """
        Process the limit model.
        """
        if amount is not None and currency is not None:
            return model(
                amount=amount,
                currency=currency,
            )
        elif amount == "null" and currency == "null":
            return "null"
        return None

    def __check_sandbox(self):
        """
        Check if the sandbox is enabled.

        Raises
        ------
        InvalidEnvironmentException
            If the sandbox is enabled.
        """
        if self.client.sandbox:
            raise InvalidEnvironmentException(
                "This feature is not available in Sandbox."
            )
