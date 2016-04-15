# README #

Simple Python helper for API authentication using HMAC token/

### Installation ###

Just add this repo to your requirements.xt

```
-e git+https://bitbucket.org/angelcam/python-hmac-toknes.git#egg=hmac_tokens
```

and run

```
pip install -r requirements.txt
```

### Usage ###

```
from hmac_tokens import verify_token

verify_token(token, secret)
```

Time and timeout attributes are automatically verified. If you need to verify addition attributes, pass them as kwargs, e.g. ```verify_token(token, secret, alias=123)```.

Rtspcon uses higher-precision timestamps which can be enabled by ```picosecods=True``.

### TODO ###

* Add client-side token generation
* Add more tests
