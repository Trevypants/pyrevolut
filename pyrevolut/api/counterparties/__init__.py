"""Manage counterparties that you intend to transact with.

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

Reference link: https://developer.revolut.com/docs/business/counterparties
"""

# flake8: noqa: F401
from .endpoint import EndpointCounterpartiesSync, EndpointCounterpartiesAsync
