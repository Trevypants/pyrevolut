"""Use payout links to send money without having to request full banking details of the recipient.
The recipient must claim the money before the link expires.

Reference link: https://developer.revolut.com/docs/business/payout-links
"""

# flake8: noqa: F401
from .endpoint import EndpointPayoutLinksSync, EndpointPayoutLinksAsync
