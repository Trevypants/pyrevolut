"""This module contains the exceptions that are raised by the pyrevolut package."""

# flake8: noqa: F401

from .common import PyRevolutBaseException
from .bad_request import PyRevolutBadRequest
from .conflict import PyRevolutConflict
from .forbidden import PyRevolutForbidden
from .internal_server_error import PyRevolutInternalServerError
from .invalid_environment import PyRevolutInvalidEnvironment
from .invalid_payload import PyRevolutInvalidPayload
from .method_not_allowed import PyRevolutMethodNotAllowed
from .network_error import PyRevolutNetworkError
from .not_acceptable import PyRevolutNotAcceptable
from .not_found import PyRevolutNotFound
from .server_unavailable import PyRevolutServerUnavailable
from .timeout_error import PyRevolutTimeoutError
from .too_many_requests import PyRevolutTooManyRequests
from .unauthorized import PyRevolutUnauthorized
