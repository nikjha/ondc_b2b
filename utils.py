from cryptography.hazmat.primitives.asymmetric import ed25519
import base64
import datetime
import os
import json
import hashlib

def hash_message(msg: str):
    digest = hashlib.blake2b(msg.encode(), digest_size=64).digest()
    digest_base64 = base64.b64encode(digest).decode()
    return digest_base64

def create_signing_string(digest_base64, created=None, expires=None):
    if created is None:
        created = int(datetime.datetime.now().timestamp())
    if expires is None:
        expires = int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
    signing_string = f"(created): {created}\n(expires): {expires}\ndigest:BLAKE-512={digest_base64}"
    return signing_string

def sign_response(json_response, created=1693301415, expires=1693387815):
    signing_string = create_signing_string(hash_message(json.dumps(json_response)), created=created, expires=expires)

    # Deserialize the private key from base64
    private_key_base64 = os.getenv("private_signing_key")
    existing_private_key_bytes = base64.b64decode(private_key_base64)

    # Ensure that the private key is 32 bytes long
    if len(existing_private_key_bytes) != 32:
        raise ValueError("Invalid private key length")

    # Create a cryptography private key object
    existing_private_key = ed25519.Ed25519PrivateKey.from_private_bytes(existing_private_key_bytes)

    # Sign the message and convert the signature to hex
    signature = existing_private_key.sign(signing_string.encode()).hex()
    return signature, created, expires

if __name__ == '__main__':
    hash_message('{"context":{"domain":"nic2004:60212","country":"IND","city":"Kochi","action":"search","core_version":"0.9.1","bap_id":"bap.stayhalo.in","bap_uri":"https://8f9f-49-207-209-131.ngrok.io/protocol/","transaction_id":"e6d9f908-1d26-4ff3-a6d1-3af3d3721054","message_id":"a2fe6d52-9fe4-4d1a-9d0b-dccb8b48522d","timestamp":"2022-01-04T09:17:55.971Z","ttl":"P1M"},"message":{"intent":{"fulfillment":{"start":{"location":{"gps":"10.108768, 76.347517"}},"end":{"location":{"gps":"10.102997, 76.353480"}}}}}}')
    request_body = {"context": {"domain": "nic2004:60212", "country": "IND", "city": "Kochi", "action": "search",
                                "core_version": "0.9.1", "bap_id": "bap.stayhalo.in",
                                "bap_uri": "https://8f9f-49-207-209-131.ngrok.io/protocol/",
                                "transaction_id": "e6d9f908-1d26-4ff3-a6d1-3af3d3721054",
                                "message_id": "a2fe6d52-9fe4-4d1a-9d0b-dccb8b48522d",
                                "timestamp": "2022-01-04T09:17:55.971Z", "ttl": "P1M"}, "message": {"intent": {
        "fulfillment": {"start": {"location": {"gps": "10.108768, 76.347517"}},
                        "end": {"location": {"gps": "10.102997, 76.353480"}}}}}}
    # Generate a new Ed25519 private key
    import nacl.signing
    private_key = nacl.signing.SigningKey.generate()

    # Serialize the private key to bytes
    # private_key_bytes = private_key.private_bytes(
    #     encoding=ed25519.Encoding.Raw,
    #     format=ed25519.PrivateFormat.Raw,
    #     encryption_algorithm=ed25519.NoEncryption()
    # )
    private_key_bytes = private_key.encode()

    # Encode the private key as base64
    private_key_base64 = base64.b64encode(private_key_bytes).decode()

    # Print the base64 encoded private key
    print(private_key_base64)

    os.environ["private_signing_key"] = private_key_base64
    x = sign_response(request_body)
    print(x)
