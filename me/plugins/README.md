# Module - Tink 
*get transactions from bank*
## Steps to work with your data

### 1. Create a user

#### a) Get Access token

Template :
```bash
curl -v -X POST https://api.tink.com/api/v1/oauth/token \
-d 'client_id={YOUR_CLIENT_ID}' \
-d 'client_secret={YOUR_CLIENT_SECRET}' \
-d 'grant_type=client_credentials' \
-d 'scope=user:create,authorization:grant'
```


Request : (Get information from https://console.tink.com/app-settings/client)
```bash
curl -v -X POST https://api.tink.com/api/v1/oauth/token \
-d 'client_id=c5db78c20d154d5a979648f12ac7182b' \
-d 'client_secret={HIDDEN_CLIENT_SECRET}' \
-d 'grant_type=client_credentials' \
-d 'scope=user:create,authorization:grant'
```

Result Access Token : ```eyJhbGciOiJFUzI1NiIsImtpZCI6IjhkYTMyM2QyLTJjNjctNGZjMi1iYmFjLTNjZmYxNThiYzc5YSIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDI3MDMwOTgsImlhdCI6MTY0MjcwMTI5OCwiaXNzIjoidGluazovL2F1dGgiLCJqdGkiOiJhOTNiZjVjOC1iMzA5LTQ0ZTYtYmVmNC0wMDZiODFjYmUyYTAiLCJzY29wZXMiOlsidXNlcjpjcmVhdGUiLCJhdXRob3JpemF0aW9uOmdyYW50Il0sInN1YiI6InRpbms6Ly9hdXRoL2NsaWVudC9jNWRiNzhjMjBkMTU0ZDVhOTc5NjQ4ZjEyYWM3MTgyYiIsInRpbms6Ly9hcHAvaWQiOiI3YTg3MzViMzgzZTE0YjJiYmRjNjAxODMwOWMzZDMzNSIsInRpbms6Ly9hcHAvdmVyaWZpZWQiOiJmYWxzZSJ9.ayV20zO5NWmMuh3YFbnlgb27qj-1Lvp-1vJQ5HbtCe1BiISUDMgz_bzDZd0wfe4Ch8VcIAbUxef6Lt5c-Vz1vw```

#### b) Create user

Template :
````bash
curl -v -X POST https://api.tink.com/api/v1/user/create \
-H 'Authorization: Bearer {YOUR_CLIENT_ACCESS_TOKEN}' \
-H 'Content-Type: application/json' \
-d '
    {
      "external_user_id": "user_123_abc",
      "market": "GB", 
      "locale": "en_US"
    }
  '
````


Request :
````bash
curl -v -X POST https://api.tink.com/api/v1/user/create \
-H 'Authorization: Bearer eyJhbGciOiJFUzI1NiIsImtpZCI6IjhkYTMyM2QyLTJjNjctNGZjMi1iYmFjLTNjZmYxNThiYzc5YSIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDI3MDMwOTgsImlhdCI6MTY0MjcwMTI5OCwiaXNzIjoidGluazovL2F1dGgiLCJqdGkiOiJhOTNiZjVjOC1iMzA5LTQ0ZTYtYmVmNC0wMDZiODFjYmUyYTAiLCJzY29wZXMiOlsidXNlcjpjcmVhdGUiLCJhdXRob3JpemF0aW9uOmdyYW50Il0sInN1YiI6InRpbms6Ly9hdXRoL2NsaWVudC9jNWRiNzhjMjBkMTU0ZDVhOTc5NjQ4ZjEyYWM3MTgyYiIsInRpbms6Ly9hcHAvaWQiOiI3YTg3MzViMzgzZTE0YjJiYmRjNjAxODMwOWMzZDMzNSIsInRpbms6Ly9hcHAvdmVyaWZpZWQiOiJmYWxzZSJ9.ayV20zO5NWmMuh3YFbnlgb27qj-1Lvp-1vJQ5HbtCe1BiISUDMgz_bzDZd0wfe4Ch8VcIAbUxef6Lt5c-Vz1vw' \
-H 'Content-Type: application/json' \
-d '
    {
      "external_user_id": "cyprien_ricque",
      "market": "FR", 
      "locale": "fr_FR"
    }
  '
````

Result :
````bash
{
  "user_id" : "e0d6a30f747549debadd589a01b684a2",
  "external_user_id" : "cyprien_ricque"
}
````

### Generate a user authorization code

> Please not that we use the same TOKEN because we specified *authorization:grant* in the scope of the token previously generated, if not we would have to generate another one

Template :
`````bash
curl -v -X POST https://api.tink.com/api/v1/oauth/authorization-grant/delegate \
-H 'Authorization: Bearer {YOUR_CLIENT_ACCESS_TOKEN}' \
-d 'response_type=code' \
-d 'actor_client_id=df05e4b379934cd09963197cc855bfe9' \
-d 'user_id=USER_ID_OPTIONAL' \
-d 'external_user_id=YOUR_OWN_ID_OPTIONAL' \
-d 'id_hint=End user name/username' \
-d 'scope=authorization:read,authorization:grant,credentials:refresh,credentials:read,credentials:write,providers:read,user:read'
`````

> Please note that *actor_client_id* in the next request is a constant for tink

Request :
````bash
curl -v -X POST https://api.tink.com/api/v1/oauth/authorization-grant/delegate \
-H 'Authorization: Bearer eyJhbGciOiJFUzI1NiIsImtpZCI6ImIzY2U0MjQ1LWNhYzQtNDJmYS1iOGNkLTk0Y2ZjMzM2ZmFiOSIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDM3NjI1MjMsImlhdCI6MTY0Mzc2MDcyMywiaXNzIjoidGluazovL2F1dGgiLCJqdGkiOiIxZTE4ZjY4MC1jODI2LTRkMmQtYjJjNS1kOWZlZWZkYTNkYTkiLCJzY29wZXMiOlsidXNlcjpjcmVhdGUiLCJhdXRob3JpemF0aW9uOmdyYW50Il0sInN1YiI6InRpbms6Ly9hdXRoL2NsaWVudC9jNWRiNzhjMjBkMTU0ZDVhOTc5NjQ4ZjEyYWM3MTgyYiIsInRpbms6Ly9hcHAvaWQiOiI3YTg3MzViMzgzZTE0YjJiYmRjNjAxODMwOWMzZDMzNSIsInRpbms6Ly9hcHAvdmVyaWZpZWQiOiJmYWxzZSJ9.CIGautiCXckqby9fy3CuYVffZuNjkfgJAkrKR53ocbv8KUwpCfmj4BekqrHBKV1E5T43MGaRWiHg5wUNdE-2ew' \
-d 'response_type=code' \
-d 'actor_client_id=df05e4b379934cd09963197cc855bfe9' \
-d 'external_user_id=cyprien_ricque' \
-d 'id_hint=Cyprien Ricque' \
-d 'scope=authorization:read,authorization:grant,credentials:refresh,credentials:read,credentials:write,providers:read,user:read'
````

Result : 
````bash
{
  "code" : "1ecaa02fe9f4494da5fa3484eb589a5e"
}
````

### Connect newly created user to its bank account

use link template link https://link.tink.com/1.0/transactions/connect-accounts?client_id={YOUR_CLIENT_ID}&state={OPTIONAL_STATE_CODE_YOU_SPECIFIED}&redirect_uri=https://console.tink.com/callback&authorization_code={USER_AUTHORIZATION_CODE}&market=GB

link : 
https://link.tink.com/1.0/transactions/connect-accounts?client_id=c5db78c20d154d5a979648f12ac7182b&redirect_uri=https://console.tink.com/callback&authorization_code=1ecaa02fe9f4494da5fa3484eb589a5e&market=FR

### Retrieve user data

credentialsId from CIC : ****************************** <br>
credentialsId from CIC 2 : ******************************* <br>
credentialsId from brsm : ********************************

**Note**: These credentialsId are never needed. When a bank account is added using the previous link, then its transactions will be added the current ones when feteching transactions.



#### a) Generate authorization code

Template : 
````bash
curl -X POST https://api.tink.com/api/v1/oauth/authorization-grant \
-H 'Authorization: Bearer {YOUR_CLIENT_ACCESS_TOKEN}' \
-d 'user_id=THE_TINK_USER_ID' \
-d 'external_user_id=YOUR_OWN_USER_ID' \
-d 'scope=accounts:read,balances:read,transactions:read,provider-consents:read,authorization:grant,balances:read,credentials:read,credentials:refresh,credentials:write,identity:read,link-session:read,link-session:write,payment:read,payment:write,provider-consents:read,providers:read,transactions:read,transfer:execute,transfer:read,user:create,user:delete,user:read,user:web_hooks,webhook-endpoints'
````

Request :
````bash
curl -X POST https://api.tink.com/api/v1/oauth/authorization-grant \
-H 'Authorization: Bearer eyJhbGciOiJFUzI1NiIsImtpZCI6IjhkYTMyM2QyLTJjNjctNGZjMi1iYmFjLTNjZmYxNThiYzc5YSIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDI3MDMwOTgsImlhdCI6MTY0MjcwMTI5OCwiaXNzIjoidGluazovL2F1dGgiLCJqdGkiOiJhOTNiZjVjOC1iMzA5LTQ0ZTYtYmVmNC0wMDZiODFjYmUyYTAiLCJzY29wZXMiOlsidXNlcjpjcmVhdGUiLCJhdXRob3JpemF0aW9uOmdyYW50Il0sInN1YiI6InRpbms6Ly9hdXRoL2NsaWVudC9jNWRiNzhjMjBkMTU0ZDVhOTc5NjQ4ZjEyYWM3MTgyYiIsInRpbms6Ly9hcHAvaWQiOiI3YTg3MzViMzgzZTE0YjJiYmRjNjAxODMwOWMzZDMzNSIsInRpbms6Ly9hcHAvdmVyaWZpZWQiOiJmYWxzZSJ9.ayV20zO5NWmMuh3YFbnlgb27qj-1Lvp-1vJQ5HbtCe1BiISUDMgz_bzDZd0wfe4Ch8VcIAbUxef6Lt5c-Vz1vw' \
-d 'external_user_id=cyprien_ricque' \
-d 'scope=accounts:read,balances:read,transactions:read,provider-consents:read,authorization:grant,balances:read,credentials:read,credentials:refresh,credentials:write,identity:read,link-session:read,link-session:write,payment:read,payment:write,provider-consents:read,providers:read,transactions:read,transfer:execute,transfer:read,user:create,user:delete,user:read,user:web_hooks,webhook-endpoints'
````

Result : 
````bash
{
  "code" : "52a08c9f78ef41e1b99a9548750350a7"
}
````

#### b) Exchange it for a user access token


Template : 
````bash
curl -v -X POST https://api.tink.com/api/v1/oauth/token \
-d 'code=YOUR_USER_AUTHORIZATION_CODE' \
-d 'client_id=YOUR_CLIENT_ID' \
-d 'client_secret=YOUR_CLIENT_SECRET' \
-d 'grant_type=authorization_code'
````

Request : 
````bash
curl -v -X POST https://api.tink.com/api/v1/oauth/token \
-d 'code=52a08c9f78ef41e1b99a9548750350a7' \
-d 'client_id=c5db78c20d154d5a979648f12ac7182b' \
-d 'client_secret={HIDDEN_CLIENT_SECRET}' \
-d 'grant_type=authorization_code'
````

Result : 
````bash
  "token_type" : "bearer",
  "expires_in" : 7200,
  "access_token" : "eyJhbGciOiJFUzI1NiIsImtpZCI6IjJkNmJiNGZkLTFlZDEtNGNjMi1hODJkLTM5NWNiYjg2MjJiOSIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDI2MjM2ODksImlhdCI6MTY0MjYxNjQ4OSwiaXNzIjoidGluazovL2F1dGgiLCJqdGkiOiI0NWIzMWY1NC04YTQ2LTQ3MmEtOTIzNC0xMDEwOGY1MzY2YWQiLCJvcmlnaW4iOiJtYWluIiwic2NvcGVzIjpbInByb3ZpZGVyczpyZWFkIiwibGluay1zZXNzaW9uOnJlYWQiLCJ1c2VyOmRlbGV0ZSIsInBheW1lbnQ6d3JpdGUiLCJiYWxhbmNlczpyZWFkIiwidHJhbnNmZXI6ZXhlY3V0ZSIsIndlYmhvb2stZW5kcG9pbnRzIiwiYWNjb3VudHM6cmVhZCIsInVzZXI6d2ViX2hvb2tzIiwiY3JlZGVudGlhbHM6cmVhZCIsInRyYW5zZmVyOnJlYWQiLCJpZGVudGl0eTpyZWFkIiwidXNlcjpjcmVhdGUiLCJwcm92aWRlci1jb25zZW50czpyZWFkIiwiY3JlZGVudGlhbHM6d3JpdGUiLCJhdXRob3JpemF0aW9uOmdyYW50IiwiY3JlZGVudGlhbHM6cmVmcmVzaCIsImxpbmstc2Vzc2lvbjp3cml0ZSIsInVzZXI6cmVhZCIsInBheW1lbnQ6cmVhZCIsInRyYW5zYWN0aW9uczpyZWFkIl0sInN1YiI6InRpbms6Ly9hdXRoL3VzZXIvZTBkNmEzMGY3NDc1NDlkZWJhZGQ1ODlhMDFiNjg0YTIiLCJ0aW5rOi8vYXBwL2lkIjoiN2E4NzM1YjM4M2UxNGIyYmJkYzYwMTgzMDljM2QzMzUiLCJ0aW5rOi8vYXBwL3ZlcmlmaWVkIjoiZmFsc2UifQ.teDhppdQ1kolPtlGrc2Flq6aWq0k6xPyJ5deLZwREiXe4vR8_1GjrfjtAvYhmkc1mHvEq7Y7BUWYdaWjWes9FA",
  "refresh_token" : "93e68ba1d57443af8e128b39f6c9d56d",
  "scope" : "providers:read,link-session:read,user:delete,payment:write,balances:read,transfer:execute,webhook-endpoints,accounts:read,user:web_hooks,credentials:read,transfer:read,identity:read,user:create,provider-consents:read,cr
edentials:write,authorization:grant,credentials:refresh,link-session:write,user:read,payment:read,transactions:read",
  "id_hint" : ""
}
````

### Redo each time

GET TOKEN

````bash
curl -v -X POST https://api.tink.com/api/v1/oauth/token \
-d 'client_id=c5db78c20d154d5a979648f12ac7182b' \
-d 'client_secret={HIDDEN_CLIENT_SECRET}' \
-d 'grant_type=client_credentials' \
-d 'credentialsId=21f311036b5d4db7907256c8fab2d7e0' \
-d 'scope=user:create,authorization:grant'
````


GENERATE AUTH CODE

````bash
curl -X POST https://api.tink.com/api/v1/oauth/authorization-grant \
-H 'Authorization: Bearer eyJhbGciOiJFUzI1NiIsImtpZCI6ImJhM2RiMWZlLWUyZjUtNDE1MS05OTYxLWZlMWVkNzBjMmNlNyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDM2NTY4MjUsImlhdCI6MTY0MzY1NTAyNSwiaXNzIjoidGluazovL2F1dGgiLCJqdGkiOiI2NmE0MmY3Mi01ZTlmLTRiZDAtOGIzNy1hMWQ5M2E1MWM1YWEiLCJzY29wZXMiOlsidXNlcjpjcmVhdGUiLCJhdXRob3JpemF0aW9uOmdyYW50Il0sInN1YiI6InRpbms6Ly9hdXRoL2NsaWVudC9jNWRiNzhjMjBkMTU0ZDVhOTc5NjQ4ZjEyYWM3MTgyYiIsInRpbms6Ly9hcHAvaWQiOiI3YTg3MzViMzgzZTE0YjJiYmRjNjAxODMwOWMzZDMzNSIsInRpbms6Ly9hcHAvdmVyaWZpZWQiOiJmYWxzZSJ9.ZLYyL8TQ_DnqXWgLUCuy-DEB_xJOX5MhueQi-9kks6zBVkSek2l8uQk2OoFT0nvCNy8C1k7ztk56_X808grKNQ' \
-d 'external_user_id=cyprien_ricque' \
-d 'scope=accounts:read,balances:read,transactions:read,provider-consents:read,authorization:grant,balances:read,credentials:read,credentials:refresh,credentials:write,identity:read,link-session:read,link-session:write,payment:read,payment:write,provider-consents:read,providers:read,transactions:read,transfer:execute,transfer:read,user:create,user:delete,user:read,user:web_hooks,webhook-endpoints'
````

GET TOKEN FROM CODE

````bash
curl -v -X POST https://api.tink.com/api/v1/oauth/token \
-d 'code=b5a910e66d4a4efcb13cb144c04fab32' \
-d 'client_id=c5db78c20d154d5a979648f12ac7182b' \
-d 'client_secret={HIDDEN_CLIENT_SECRET}' \
-d 'grant_type=authorization_code'
````
