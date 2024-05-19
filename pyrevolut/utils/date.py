from typing import Type, Any
import datetime

import pendulum
from pendulum import Date as _Date  # type: ignore

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class Date(_Date):
    """A `pendulum.Date` object for Pydantic validation."""

    __slots__: list[str] = []

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Return a Pydantic CoreSchema with the Date validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the Date validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate, core_schema.datetime_schema()
        )

    @classmethod
    def _validate(
        cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler
    ) -> Any:
        """
        Validate the date object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError.
        """
        # if we are passed an existing instance, pass it straight through.
        if isinstance(value, _Date):
            return handler(value)

        # otherwise, parse it.
        try:
            data = to_date(value)
        except Exception as exc:
            raise PydanticCustomError("value_error", str(exc)) from exc  # type: ignore
        return handler(data)


def to_date(dt: datetime.date | _Date | str) -> Date:
    """Converts various date representations to a pendulum Date object.

    Parameters
    ----------
    dt : datetime.date | Date | str
        The object to be converted.

    Returns
    -------
    Date
        The pendulum Date object.
    """
    if isinstance(dt, datetime.date):
        return pendulum.Date(year=dt.year, month=dt.month, day=dt.day)
    elif isinstance(dt, str):
        return string_to_date(dt)
    else:
        raise ValueError(
            f"Unsupported type for conversion to pendulum Date: {type(dt)}"
        )


def string_to_date(string: str) -> Date:
    """Converts a string to a pendulum Date object.

    Parameters
    ----------
    string : str
        The string to be converted.

    Returns
    -------
    Date
        The pendulum Date object.
    """
    formats = [
        "YYYY-MM-DD",
        "YYYY/MM/DD",
        "YYYY.MM.DD",
        "YYYYMMDD",
        "YYYY-MM",
        "YYYY/MM",
        "YYYY.MM",
        "YYYYMM",
        "YYYY",
        "MM-YYYY",
        "MM/YYYY",
        "MM.YYYY",
        "MMYYYY",
    ]
    for format in formats:
        try:
            return pendulum.from_format(string=string, fmt=format, tz="UTC")
        except Exception:
            pass
    raise PydanticCustomError(f"Error converting string to pendulum Date: {string}")
