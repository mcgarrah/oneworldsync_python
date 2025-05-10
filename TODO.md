# TODO

- [ ] make environment variable less generalized so no overlap
- [ ] find the demo pre-prod credentials from documentation
- [ ] add `pytest` for automated testing
- [ ] links to 1ws PDF documents and not the actual files
- [ ] setup PyPi account
- [ ] `.github` for PyPi packaging and Github management
- [ ] MORE THINKING NEEDED HERE

## DotEnv Fix

``` ini
# PROD - OneWorldSync APP_ID/SECRET_KEY
# ONEWORLDSYNC_SERVER_URL='https://marketplace.api.1worldsync.com/V2/products'
# ONEWORLDSYNC_CLIENT_ID='my-expensive-app-id'
# ONEWORLDSYNC_CLIENT_SECRET='my-expensive-secret-key'

# PRE-PROD - OneWorldSync APP_ID/SECRET_KEY
# ONEWORLDSYNC_SERVER_URL='https://marketplace.preprod.api.1worldsync.com/V2/products'
# ONEWORLDSYNC_CLIENT_ID='my-free-app-id'
# ONEWORLDSYNC_CLIENT_SECRET='my-free-secret-key'

# DEMO - OneWorldSync APP_ID/SECRET_KEY
# ONEWORLDSYNC_SERVER_URL='https://marketplace.preprod.api.1worldsync.com/V2/products'
# ONEWORLDSYNC_CLIENT_ID='my-demo-app-id'
# ONEWORLDSYNC_CLIENT_SECRET='my-demo-secret-key'
```
