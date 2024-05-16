# (Transfer)Wise Python SDK

This is an un-official Python SDK for the [Revolut Business API](https://developer.revolut.com/docs/business/business-api).

## Installation

```bash
pip install TO-BE-DEFINED
```

## Usage

### Basic Usage

```python
from pyrevolut.client import Client, Environment

ACCESS_TOKEN = "YOUR-ACCESS-TOKEN"
REFRESH_TOKEN = "YOUR-REFRESH-TOKEN"

client = Client(
    access_token=ACCESS_TOKEN,
    refresh_token=REFRESH_TOKEN,
    environment=Environment.SANDBOX,
)

# Initialize the client
client.open()

# List all accounts for the authenticated user
accounts = client.Accounts.get_all_accounts()

# Close the client
client.close()

# You can also use the client as a context manager
with Client(access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN, environment=Environment.SANDBOX) as client:
    accounts = client.Accounts.get_all_accounts()
```

### Advanced Usage

It is possible to use the client asynchronously by using the `async` keyword.
All synchronous methods have an asynchronous counterpart with the `a` prefix.

```python
import asyncio
from pyrevolut.client import Client, Environment

ACCESS_TOKEN = "YOUR-ACCESS-TOKEN"
REFRESH_TOKEN = "YOUR-REFRESH-TOKEN"

client = Client(
    access_token=ACCESS_TOKEN,
    refresh_token=REFRESH_TOKEN,
    environment=Environment.SANDBOX,
)

# Run without context manager
async def run():
    await client.aopen() # <-- Note the `a` prefix
    accounts = await client.Accounts.aget_all_accounts() # <-- Note the `a` prefix
    await client.aclose() # <-- Note the `a` prefix
    return accounts

# Run with context manager
async def run_context_manager():
    async with client:
        accounts = await client.Accounts.aget_all_accounts() # <-- Note the `a` prefix
    return accounts

# List all accounts for the authenticated user
accounts = asyncio.run(run())
accounts_context_manager = asyncio.run(run_context_manager())

```

## API Support Status

The SDK currently supports the following APIs:

- [ ] Accounts
  - [ ] Retrieve all accounts
  - [ ] Retrieve an account
  - [ ] Retrieve account's full bank details
- [ ] Cards
  - [ ] Retrieve a list of cards
  - [ ] Create a card
  - [ ] Retrieve card details
  - [ ] Update card details
  - [ ] Terminate a card
  - [ ] Freeze a card
  - [ ] Unfreeze a card
  - [ ] Retrieve sensitive card details
- [ ] Counterparties
  - [ ] Retrieve a list of counterparties
  - [ ] Retrieve a counterparty
  - [ ] Delete a counterparty
  - [ ] Create a counterparty
  - [ ] Validate an account name (CoP)
- [ ] Foreign exchange
  - [ ] Get an exchange rate
  - [ ] Exchange money
- [ ] Payment drafts
  - [ ] Retrieve all payments drafts
  - [ ] Create a payment draft
  - [ ] Retrieve a payment draft
  - [ ] Delete a payment draft
- [ ] Payout links
  - [ ] Retrieve a list of payout links
  - [ ] Retrieve a payout link
  - [ ] Create a payout link
  - [ ] Cancel a payout link
  - [ ] Get transfer reasons
- [ ] Simulations
  - [ ] Simulate a transfer state update (Sandbox only)
  - [ ] Simulate an account top-up (Sandbox only)
- [ ] Team members
  - [ ] Retrieve a list of team members
  - [ ] Invite a new memebr to your business
  - [ ] Retrieve team roles
- [ ] Transactions
  - [ ] Retrieve a list of transactions
  - [ ] Retrieve a transaction
- [ ] Transfers
  - [ ] Move money between your accounts
  - [ ] Create a transfer to another account
  - [ ] Get transfer reasons
- [ ] Webhooks (v2)
  - [ ] Create a new webhook
  - [ ] Retrieve a list of webhooks
  - [ ] Retrieve a webhook
  - [ ] Update a webhook
  - [ ] Delete a webhook
  - [ ] Rotate a webhook signing secret
  - [ ] Retrieve a list of failed webhook events

## **Contributing**

In order to facilitate a streamlined development process, we have a few guidelines that we would like to follow. Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.
