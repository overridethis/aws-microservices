#!/bin/sh

# GET TOKEN ON BROWSER
#  https://COGNITO_USER_POOL.auth.us-east-2.amazoncognito.com/login?response_type=token&client_id=CLIENT_ID&scope=email+profile&redirect_uri=https://jwt.io

# data.
CLIENT_ID={{REPLACE_WITH_CLIENTID}}
PASSWORD="{{REPLACE_WITH_PASSWORD}}"

# get token
aws cognito-idp initiate-auth \
    --region us-east-2 --auth-flow USER_PASSWORD_AUTH \
    --client-id $CLIENT_ID \
    --auth-parameters USERNAME=roberto.hernandez@infernored.com,PASSWORD=$PASSWORD \
    --profile infernored 
