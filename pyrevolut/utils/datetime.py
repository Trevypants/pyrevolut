from typing import Type, Any
import datetime

import pendulum
from pendulum import DateTime as _DateTime  # type: ignore
from pendulum.exceptions import PendulumException

from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema


class DateTime(_DateTime):
    """
    A `pendulum.DateTime` object. At runtime, this type decomposes into pendulum.DateTime automatically.
    This type exists because Pydantic throws a fit on unknown types.
    """

    __slots__: list[str] = []

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Return a Pydantic CoreSchema with the DateTime validation

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the DateTime validation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls._validate, core_schema.datetime_schema()
        )

    @classmethod
    def _validate(
        cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler
    ) -> Any:
        """
        Validate the datetime object and return it.

        Args:
            value: The value to validate.
            handler: The handler to get the CoreSchema.

        Returns:
            The validated value or raises a PydanticCustomError.
        """
        # if we are passed an existing instance, pass it straight through.
        if isinstance(value, _DateTime):
            return handler(value)

        # otherwise, parse it.
        try:
            data = to_datetime(value)
        except Exception as exc:
            raise PydanticCustomError("value_error", str(exc)) from exc  # type: ignore
        return handler(data)


def to_datetime(
    dt: datetime.datetime | _DateTime | str | int | float, timestamp_unit: str = "ms"
):
    """
    Converts a datetime object or string to a pendulum DateTime object.

    Parameters
    ----------
    dt : datetime | DateTime | str | int | float
        The object to be converted.
    timestamp_unit : str, optional
        The unit of the timestamp. The default is 'ms'.

    Returns
    -------
    DateTime
        The pendulum DateTime object.

    """
    if isinstance(dt, datetime.datetime):
        new_dt: DateTime = pendulum.instance(dt, tz="UTC")  # type: ignore
    elif isinstance(dt, str):
        new_dt: DateTime = string_to_datetime(dt)
    elif isinstance(dt, int) or isinstance(dt, float):
        new_dt: DateTime = timestamp_to_datetime(dt, unit=timestamp_unit)
    new_dt: DateTime = pendulum.instance(new_dt, tz="UTC")  # type: ignore
    return new_dt


def timestamp_to_datetime(
    timestamp: float | int,
    unit: str = "ms",
):
    """
    Converts a timestamp to a pendulum DateTime object.

    Parameters
    ----------
    timestamp : float | int
        The timestamp to be converted.
    unit : str, optional
        The unit of the timestamp. The default is 'ms'.

    Returns
    -------
    DateTime
        The pendulum DateTime object.

    Raises
    ------
    ValueError
        If the unit is not supported.

    """
    if unit == "ms":
        dt: DateTime = pendulum.from_timestamp(timestamp / 1000, tz="UTC")  # type: ignore
    elif unit == "s":
        dt: DateTime = pendulum.from_timestamp(timestamp, tz="UTC")  # type: ignore
    else:
        raise ValueError(f"Unsupported unit: {unit}")
    return dt


def string_to_datetime(string: str):
    """
    Converts a string to a pendulum DateTime object.

    Parameters
    ----------
    string : str
        The string to be converted.

    Returns
    -------
    DateTime
        The pendulum DateTime object.

    Raises
    ------
    ValueError
        If the string cannot be converted to a pendulum DateTime object.

    """
    try:
        dt: DateTime = pendulum.parser.parse(string).in_timezone("UTC")  # type: ignore
        return dt
    except PendulumException as exc:
        raise ValueError(f"Could not parse string: {string}") from exc
