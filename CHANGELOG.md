## v0.9.1 (2024-06-10)

### Refactor

- remove access token refresh on client init

## v0.9.0 (2024-06-07)

### Feat

- added option to specify a custom save/load function for credentials

## v0.8.0 (2024-06-05)

### Feat

- added ability to provide creds as dict or base64 encoded string

### Fix

- allow request id response to have more than 40 characters

## v0.7.1 (2024-06-02)

### Fix

- fixed ngrok auth token

## v0.7.0 (2024-06-01)

### Feat

- added a webhooks function to receive webhook payload data

## v0.6.2 (2024-05-20)

### Fix

- dependency fix

## v0.6.1 (2024-05-19)

### Fix

- replaced all decimals with floats

## v0.6.0 (2024-05-19)

### Feat

- added options to specify how to handle errors
- added option to choose output type between 'raw', 'dict', and 'model'
- added client option to return pydantic models instead of dicts

## v0.5.1 (2024-05-19)

### Refactor

- fixed payout links test file name

## v0.5.0 (2024-05-18)

### Feat

- added auth features with CLI
- added auth cli commands

### Refactor

- split sync and async into their own clients

## v0.4.0 (2024-05-17)

### Feat

- added webhooks endpoints
- added transfers endpoint
- added transactions endpoint
- added team members endpoint
- added simulations endpoint
- added payout links endpoint
- added payment drafts endpoint
- added foreign exchange endpoint
- added counterparties endpoint
- added cards endpoint

## v0.3.0 (2024-05-16)

### Feat

- added accounts endpoint

## v0.2.0 (2024-05-16)

### Feat

- init commit
