# Credentials

## Revolut

For testing purposes, place your Revolut credentials in this directory. They will be ignored by git.
It is possible to place multiple credentials files in this directory, as long as they have the same format.
The tests will randomly pick one of the files per test.

## Environment Variables

The testing environment will look for an .env file in this directory. The file should contain the following variables:

```bash
NGROK_AUTH_TOKEN=2hK5kZLB9b5w9IhW6eXp8uP4Ri1_7sMkjEw8WDLUQoL93DbgY
```

The NGROK_AUTH_TOKEN is used to authenticate the ngrok tunnel so the tests can run against the local server.
