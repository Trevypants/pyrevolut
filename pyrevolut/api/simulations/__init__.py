"""The Simulations API is only available in the Sandbox environment.
It lets you simulate certain events that are otherwise only possible in the production environment,
such as your account's top-up and transfer state changes.

Reference link: https://developer.revolut.com/docs/business/simulations
"""

# flake8: noqa: F401
from .endpoint import EndpointSimulationsSync, EndpointSimulationsAsync
