# Mission 098 - Encode the API Key
import base64

def encode_credentials(user, password):
    """Return base64-encoded 'user:password' as a string."""
    combined = f"{user}:{password}"
    return base64.b64encode(combined.encode())

if __name__ == "__main__":
    token = encode_credentials("admin", "s3cr3t")
    print(type(token), token)
