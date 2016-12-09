import base64
import hashlib
import hmac
import time
import json

def debug(msg):
    return
    print(msg)

#returns (data in base64, HMAC in hexdigest)
def encode(data, secret):
    data_b64 = base64.b64encode(data.encode('utf-8'))
    sig = hmac.new(secret.encode('utf-8'), data_b64, hashlib.sha256)
    return (data_b64, sig.hexdigest())

def decode_token(token, secret, microseconds=False):
    """
    Verify a given token and return its content. The method returns a
    dictionary containing token fields or None if the token is invalid.

    Checks that the:
    - message is signed with proper secret
    - timeout is not experied
    """
    if not (token and secret):
        return None

    parts = token.split(".")
    if len(parts) != 2:
        debug("Message or signature missing")
        return None

    try:
        message_b64, client_sig = parts
        message = base64.b64decode(message_b64).decode('utf-8')

        # encode message with server key for verification
        server_sig = encode(message, secret)[1]

        if client_sig != server_sig:
            debug("Signature verification failed")
            return None

        payload = json.loads(message)

        if not (payload["time"] and payload["timeout"]):
            debug("Time of timeout missing")
            return None

        payload_time = int(payload["time"])
        if microseconds:
            payload_time = payload_time / 1000000

        payload_timeout = int(payload["timeout"])

        current = int(time.time())

        if not (payload_time - payload_timeout <= current <= payload_time + 2 * payload_timeout):
            debug("Time validation failed")
            return None

        return payload

    except Exception as e:
        debug("Invalid data received: %s" % e)
        return None

def verify_token(token, secret, microseconds=False, **kwargs):
    """
    Verify the HMAC token sent by client.

    Checks that the:
    - message is signed with proper secret
    - timeout is not experied
    - any additional kwargs are present in the message (e.g. camera alias)
    """
    payload = decode_token(token, secret, microseconds)
    if payload is None:
        return False

    # check if the message contains all attributes from kwargs (and their values)
    for arg in kwargs:
        if payload.get(arg, None) != kwargs[arg]:
            debug("Extra field %s verification failed" % arg)
            return False

    return True

def gen_token(secret, token_time=None, timeout=60, microseconds=False, **kwargs):
    """
    Generate HMAC token to be sent to server.

    Arguments
    - token_time: if no time is provided, use current time
    - timeout: validity of the token in seconds
    - microseconds: use microseconds precision (for rtspcon)
    - all other kwargs are added to the token (e.g. camera_id,...)
    """

    if not secret:
        raise ValueError("Secret is required")

    if not token_time:
        token_time = time.time()

    if microseconds:
        token_time = token_time * 1000000

    token_time = int(token_time)

    payload = {
        'time': token_time,
        'timeout' : timeout,
    }

    for arg in kwargs:
       payload[arg] = kwargs[arg]

    parts = encode(json.dumps(payload), secret)
    return "{}.{}".format(parts[0].decode('utf-8'), parts[1])
