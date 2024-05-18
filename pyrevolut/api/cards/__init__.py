"""Manage cards for the business team members, freeze, unfreeze,
terminate and update card settings, such as transaction limits.

This feature is available in the UK, US and the EEA.
This feature is not available in Sandbox.

Reference link: https://developer.revolut.com/docs/business/cards
"""

# flake8: noqa: F401
from .endpoint import EndpointCardsSync, EndpointCardsAsync
