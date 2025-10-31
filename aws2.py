import requests
import hashlib
from urllib.parse import urlencode
from datetime import datetime

# OAuth authorization endpoint (where redirect_uri is validated)
auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
client_id = "<your_client_id>"

# Redirect URI test cases - testing for permissive prefix matching
redirect_uri_variants = {
    "legitimate": "https://hyatt.com/oauth/callback",
    "open_redirect": "https://hyatt.com/redirect?url=https://attacker.com/steal",
    "path_traversal": "https://hyatt.com/../attacker.com/callback",
    "subdomain_bypass": "https://hyatt.com.attacker.com/callback",
    "path_append": "https://hyatt.com/oauth/callback@attacker.com",
    "query_injection": "https://hyatt.com/callback?next=https://attacker.com",
    "fragment_injection": "https://hyatt.com/callback#https://attacker.com"
}

headers = {
    "User-Agent": "FreeBoldSec-CallbackScanner/1.1",
    "Accept": "*/*"
}

def hash_body(body):
    return hashlib.sha256(body.encode('utf-8')).hexdigest()

# Run tests
for label, redirect_uri in redirect_uri_variants.items():
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": "test_state_123"
    }
    full_url = f"{auth_url}?{urlencode(params)}"
    
    print(f"\n🔍 [{datetime.utcnow()}] Testing '{label}' redirect_uri variant:")
    print(f"URL: {full_url}")
    
    try:
        response = requests.get(full_url, headers=headers, timeout=10, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        
        # Redirect tracking
        if response.history:
            print("🔁 Redirect Chain:")
            for r in response.history:
                print(f"  {r.status_code} → {r.url}")
            print(f"  Final URL: {response.url}")
        else:
            print("🔁 No redirects detected.")
        
        # Cookie inspection
        cookies = response.cookies.get_dict()
        print("🍪 Cookies:")
        if cookies:
            for k, v in cookies.items():
                print(f"  {k}: {v}")
        else:
            print("  None")
        
        # Header fingerprint
        print("📡 Headers:")
        for k, v in response.headers.items():
            print(f"  {k}: {v}")
        
        # Body hash
        body = response.text
        body_hash = hash_body(body)
        print(f"🧬 Body SHA256: {body_hash}")
        
        # Vulnerability detection
        if response.status_code == 200 and "consent" in body.lower():
            print("🚨 VULNERABLE: redirect_uri accepted - consent screen shown!")
        elif response.status_code in [302, 301, 303, 307, 308]:
            location = response.headers.get('Location', '')
            if redirect_uri in location or "attacker.com" in location:
                print("🚨 VULNERABLE: Redirect accepted with malicious redirect_uri!")
            else:
                print("✅ Redirect occurred but to different location")
        elif "redirect_uri_mismatch" in body.lower() or "invalid" in body.lower():
            print("✅ SECURE: redirect_uri rejected")
        else:
            print("⚠️ Unexpected response - manual review needed")

    except Exception as e:
        print(f"⚠️ Request failed: {e}")
