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
    local_storage=f"abc_personalized_token.json"
)
# create new entry in globals, using the provider name as key
print(f"first token: {ltm_three.get_token()}")


print(f"Fetching token from APIC CLOUD API in wiremock - JSON")
ltm_three = LightTokenManager(
    "https://cloud-apic.wiremockapi.cloud/api/token",
    "aaa",
    "bbb",
    "profile",
    "client_credentials",
    payload_format="json",
    local_storage = f"apic_cloud_json_token.json"
)
print(f"first token: {ltm_three.get_token()}")


print(f"Fetching token from APIC CLOUD API in wiremock - YAML")
ltm_three = LightTokenManager(
    "https://cloud-apic.wiremockapi.cloud/api/token",
    "aaa",
    "bbb",
    grant_type="client_credentials",
    payload_format="yaml",
    local_storage = f"apic_cloud_yaml_token.json"
)
# create new entry in globals, using the provider name as key
print(f"first token: {ltm_three.get_token()}")



print(f"Fetching token from APIC CLOUD API in wiremock - using body arg")
ltm_three = LightTokenManager(
    "https://cloud-apic.wiremockapi.cloud/api/token",
    payload_format="json",
    body={
        "client_id": "aaa",
        "client_secret": "bbb",
        "grant_type": "client_credentials",
        "realm": "admin/amta"
    },
    local_storage = f"apic_cloud_body_token.json"
)
# create new entry in globals, using the provider name as key
print(f"first token: {ltm_three.get_token()}")

print(f"Fetching token from APIC CLOUD API in wiremock - using body arg")
ltm_three = LightTokenManager(
    "https://cloud-apic.wiremockapi.cloud/api/token",
    payload_format="json",
    body={
        "client_id": "aaa",
        "client_secret": "bbb",
        "grant_type": "client_credentials",
        "realm": "admin/amta"
    }
)
# create new entry in globals, using the provider name as key
print(f"first token: {ltm_three.get_token()}")
