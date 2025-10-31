from urllib.parse import urlparse
from typing import Set, Optional

class SecureOAuthValidator:
    def __init__(self, allowed_redirect_uris: Set[str]):
        """Initialize with exact list of pre-approved redirect URIs"""
        self.allowed_redirect_uris = allowed_redirect_uris
    
    def validate_redirect_uri(self, redirect_uri: str) -> bool:
        """
        Secure validation using exact match against pre-approved URIs
        Returns True only if redirect_uri exactly matches an allowed URI
        """
        if not redirect_uri:
            return False
            
        # Normalize the URI
        try:
            parsed = urlparse(redirect_uri)
            normalized_uri = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                normalized_uri += f"?{parsed.query}"
        except Exception:
            return False
            
        # Exact match validation
        return normalized_uri in self.allowed_redirect_uris

# Example usage with pre-approved Hyatt redirect URIs
APPROVED_REDIRECT_URIS = {
    "https://hyatt.com/oauth/callback",
    "https://hyatt.com/auth/google/callback", 
    "https://hyatt.com/login/oauth2/callback"
}

validator = SecureOAuthValidator(APPROVED_REDIRECT_URIS)

# Test cases
test_uris = [
    "https://hyatt.com/oauth/callback",  # Valid
    "https://hyatt.com/redirect?url=attacker.com",  # Attack attempt - blocked
    "https://hyatt.com/oauth/callback/../admin",  # Path traversal - blocked
    "https://evil.com",  # External domain - blocked
    "https://hyatt.com.evil.com/oauth/callback"  # Subdomain attack - blocked
]

for uri in test_uris:
    result = validator.validate_redirect_uri(uri)
    print(f"URI: {uri}")
    print(f"Valid: {result}\n")