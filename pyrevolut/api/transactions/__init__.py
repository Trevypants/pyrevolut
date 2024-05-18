"""Get the details of your transactions.

Note
----
An incoming or outgoing payment is represented as a transaction.

Reference link: https://developer.revolut.com/docs/business/team-members
"""

# flake8: noqa: F401
from .endpoint import EndpointTransactionsSync, EndpointTransactionsAsync
