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

def verify_token(token, secret, microseconds=False, **kwargs):
    """
    Verify the HMAC token sent by client.

    Checks that the:
    - message is signed with proper secret
    - timeout is not experied
    - any additional kwargs are present in the message (e.g. camera alias)
    """

    if not (token and secret):
        return False

    parts = token.split(".")
    if len(parts) != 2:
        debug("Message or signature missing")
        return False

    try:
        message_b64, client_sig = parts
        message = base64.b64decode(message_b64).decode('utf-8')

        # encode message with server key for verification
        server_sig = encode(message, secret)[1]

        if client_sig != server_sig:
            debug("Signature verification failed")
            return False

        payload = json.loads(message)

        if not (payload["time"] and payload["timeout"]):
            debug("Time of timeout missing")
            return False

        payload_time = int(payload["time"])
        if microseconds:
            payload_time = payload_time / 1000000

        payload_timeout = int(payload["timeout"])

        current = int(time.time())

        if not (payload_time - payload_timeout <= current <= payload_time + 2 * payload_timeout):
            debug("Time validation failed")
            return False

        # check the message contains all attributes from kwargs (and the value)
        for arg in kwargs:
            if payload.get(arg, None) != kwargs[arg]:
                debug("Extra field %s verification failed" % arg)
                return False

        return True

    except ValueError as e:
        debug("Invalid data received: %s" % e)
        return False

def gen_token(secret, token_time=None, timeout=60, microseconds=False, **kwargs):
    """
    Generate HMAC token to be sent to server.

    Arguments
    - token_time: if no time is provided, use current time
    - timestamp: validity of the token in seconds
    - microseconds: use microseconds precision (for rtspcon)
    - all other kwargs are added to the token (e.g. camera_id,...)
    """

    if not secret:
        raise ValueError("Secret is required")

    if not token_time:
        token_time = int(time.time())

    if microseconds:
        token_time = token_time * 1000000
        timeout = timeout * 1000000

    payload = {
        'time': token_time,
        'timeout' : timeout,
    }

    for arg in kwargs:
       payload[arg] = kwargs[arg]

    parts = encode(json.dumps(payload), secret)
    return "{}.{}".format(parts[0].decode('utf-8'), parts[1])
