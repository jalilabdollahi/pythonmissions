# Mission 098 - Solution
import base64

def encode_credentials(user, password):
    combined = f"{user}:{password}"
    return base64.b64encode(combined.encode()).decode()

if __name__ == "__main__":
    token = encode_credentials("admin", "s3cr3t")
    print(type(token), token)
