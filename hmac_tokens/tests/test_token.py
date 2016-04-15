import base64
import hashlib
import hmac
import time

from hmac_tokens import verify_token

good_secret = "1234567890abcdef1234567890abcdef"
bad_secret = "11111111111111111111111111111111"

def sign_msg(message, secret):
    msg_b64 = base64.b64encode(message)
    sig = hmac.new(secret, msg_b64, hashlib.sha256)
    return '%s.%s' % (msg_b64, sig.hexdigest())

fmt = '{ "time" : %d, "timeout" : %d }'
fmt_alias = '{ "time" : %d, "timeout" : %d, "alias" : "%s" }'

def test_basic():
    message =  fmt % (time.time(), 10)
    token = sign_msg(message, good_secret)
    assert verify_token(token, good_secret) == True

    message =  fmt % (time.time() - 21, 10)
    token = sign_msg(message, good_secret)
    assert verify_token(token, good_secret) == False

    message =  fmt % (time.time() + 11, 10)
    token = sign_msg(message, good_secret)
    assert verify_token(token, good_secret) == False

    # wrong token
    message =  fmt % (time.time(), 10)
    token = sign_msg(message, bad_secret)
    assert verify_token(token, good_secret) == True

def test_kwargs():
    message =  fmt % (time.time(), 10)
    token = sign_msg(message, good_secret)
    assert verify_token(token, good_secret, alias='foo') == False

    message =  fmt_alias % (time.time(), 10, 'foo')
    token = sign_msg(message, good_secret)
    assert verify_token(token, good_secret, alias='foo') == True
    assert verify_token(token, good_secret, alias='bar') == False
