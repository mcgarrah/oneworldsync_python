# TODO

- [x] make environment variable less generalized so no overlap
- [ ] find the demo pre-prod credentials from documentation
- [ ] add `pytest` for automated testing
- [ ] links to 1ws PDF documents and not the actual files
- [ ] setup PyPi account
- [ ] `.github` for PyPi packaging and Github management
- [ ] MORE THINKING NEEDED HERE

## DotEnv Fix

``` ini
# PROD - OneWorldSync Environment Variables
# ONEWORLDSYNC_API_URL="https://marketplace.api.1worldsync.com"
# ONEWORLDSYNC_APP_ID="my-expensive-app-id"
# ONEWORLDSYNC_SECRET_KEY="my-expensive-secret-key"

# PRE-PROD - OneWorldSync Environment Variables
# ONEWORLDSYNC_API_URL="https://marketplace.preprod.api.1worldsync.com"
# ONEWORLDSYNC_APP_ID="my-free-app-id"
# ONEWORLDSYNC_SECRET_KEY="my-free-secret-key"

# DEMO - OneWorldSync Environment Variables
# ONEWORLDSYNC_API_URL="https://marketplace.preprod.api.1worldsync.com"
# ONEWORLDSYNC_APP_ID="my-demo-app-id"
# ONEWORLDSYNC_SECRET_KEY="my-demo-secret-key"
```