# Pyrevolut: A Revolut Business API Wrapper

`pyrevolut` is an un-official wrapper around the [Revolut Business API](https://developer.revolut.com/docs/business/business-api).

## Installation

```bash
pip install TO-BE-DEFINED
```

## Usage

### Basic Usage

```python
from pyrevolut.client import Client

CREDS_JSON_LOC = "path/to/creds.json"

client = Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

# Initialize the client
client.open()

# List all accounts for the authenticated user
accounts = client.Accounts.get_all_accounts()

# Close the client
client.close()

# You can also use the client as a context manager
with Client(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True
) as client:
    accounts = client.Accounts.get_all_accounts()
```

### Advanced Usage

It is possible to use the client library asynchronously by using the `AsyncClient` object.

```python
import asyncio
from pyrevolut.client import AsyncClient

CREDS_JSON_LOC = "path/to/creds.json"

client = AsyncClient(
    creds_loc=CREDS_JSON_LOC,
    sandbox=True,
)

# Run without context manager
async def run():
    await client.open() 
    accounts = await client.Accounts.get_all_accounts()
    await client.close() 
    return accounts

# Run with context manager
async def run_context_manager():
    async with client:
        accounts = await client.Accounts.get_all_accounts() 
    return accounts

# List all accounts for the authenticated user
accounts = asyncio.run(run())
accounts_context_manager = asyncio.run(run_context_manager())

```

## Authentication

In order to make use of the Revolut Business API, you will need to go through several steps to authenticate your application. The basic guide can be found [here](https://developer.revolut.com/docs/guides/manage-accounts/get-started/make-your-first-api-request). We have provided a simple CLI tool to help you generate the necessary credentials. This tool follows the steps outlined in the guide.

```bash

pyrevolut auth-manual

```

Alternatively, you can use call the CLI via Python.

```bash

python -m pyrevolut auth-manual

```

Upon completion, you will have a `.json` file that you can use to authenticate your application.

## API Support Status

The SDK currently supports the following APIs:

- [x] Accounts
  - [x] Retrieve all accounts
  - [x] Retrieve an account
  - [x] Retrieve account's full bank details
- [ ] Cards (Live only)
  - [ ] Retrieve a list of cards
  - [ ] Create a card
  - [ ] Retrieve card details
  - [ ] Update card details
  - [ ] Terminate a card
  - [ ] Freeze a card
  - [ ] Unfreeze a card
  - [ ] Retrieve sensitive card details
- [x] Counterparties
  - [x] Retrieve a list of counterparties
  - [x] Retrieve a counterparty
  - [x] Delete a counterparty
  - [x] Create a counterparty (Personal)
  - [x] Create a counterparty (Business)
  - [x] Validate an account name (CoP)
- [ ] Foreign exchange
  - [x] Get an exchange rate
  - [ ] Exchange money
- [ ] Payment drafts
  - [x] Retrieve all payments drafts
  - [ ] Create a payment draft
  - [x] Retrieve a payment draft
  - [ ] Delete a payment draft
- [x] Payout links
  - [x] Retrieve a list of payout links
  - [x] Retrieve a payout link
  - [x] Create a payout link
  - [x] Cancel a payout link
- [x] Simulations (Sandbox only)
  - [x] Simulate a transfer state update
  - [x] Simulate an account top-up
- [ ] Team members (Live only)
  - [ ] Retrieve a list of team members
  - [ ] Invite a new memebr to your business
  - [ ] Retrieve team roles
- [x] Transactions
  - [x] Retrieve a list of transactions
  - [x] Retrieve a transaction
- [x] Transfers
  - [x] Move money between your accounts
  - [x] Create a transfer to another account
  - [x] Get transfer reasons
- [x] Webhooks (v2)
  - [x] Create a new webhook
  - [x] Retrieve a list of webhooks
  - [x] Retrieve a webhook
  - [x] Update a webhook
  - [x] Delete a webhook
  - [x] Rotate a webhook signing secret
  - [x] Retrieve a list of failed webhook events

## **Contributing**

In order to facilitate a streamlined development process, we have a few guidelines that we would like to follow. Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Disclaimer:** `pyrevolut` is an un-official API wrapper. It is in no way endorsed by or affiliated with Revolut or any associated organization. Make sure to read and understand the terms of service of the underlying API before using this package. The authors accept no responsiblity for any damage that might stem from use of this package.
