from light_token_manager.main import LightTokenManager

print(f"Fetching token from provider 1")
ltm_one = LightTokenManager(
    "https://fake-idp.wiremockapi.cloud/token",
    "aaa",
    "bbb",
    "profile",
    "client_credentials"
)
# create new entry in globals, using the provider name as key
print(f"first token: {ltm_one.get_token()}")


print(f"Fetching token from provider 2")
ltm_two = LightTokenManager(
    "https://fake-idp.wiremockapi.cloud/token_2",
    "zzz",
    "yyy",
    "profile",
    "client_credentials"
)
# create new entry in globals, using the provider name as key
print(f"first token: {ltm_two.get_token()}")

print(f"Fetching token from provider 3")
ltm_three = LightTokenManager(
    "https://fake-idp.wiremockapi.cloud/token",
    "aaa",
    "bbb",
    "profile",
    "client_credentials",
    local_storage=f"my_personalized_token.json"

)
# create new entry in globals, using the provider name as key
print(f"first token: {ltm_three.get_token()}")



