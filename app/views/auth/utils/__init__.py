import base64
import datetime
import hashlib
import hmac
import json

from typing import Literal


from flask import g
from flask import request
from flask import abort
from flask import url_for
from flask import redirect
from flask import make_response


SK = '23456789sdfghjkl4567890fdshjkld4f56gh7j89kfgrfrf343v6enu'



def auth_manager( *args, **kwargs):
    required = kwargs.get("required")
    anonimous = kwargs.get("anonimous")
    def decorator(func):
        def wrapper(*args, **kwargs):
            if required and "user" not in g:
                n = base64.b64encode(bytes(request.url.encode("utf-8")))
                return redirect(url_for("auth.login",next=n, _external=True))
            if anonimous and "user" in g: return redirect(url_for("webui.index", _external=True))
            return func(*args, **kwargs)
    
        return wrapper
    return decorator



def create_access_jwt(user, keep: bool = None):
    payload = {
        "userID": user.id,
        "exp": (datetime.datetime.now() + datetime.timedelta(minutes=30)).timestamp()
    }
    if keep: payload["exp"] = (datetime.datetime.now() + datetime.timedelta(days=365)).timestamp()

    header = json.dumps( {'typ': 'JWT', 'alg': 'HS256'} ).encode()
    payload = json.dumps(payload).encode()

    b64_header  = base64.urlsafe_b64encode(header).decode()
    b64_payload = base64.urlsafe_b64encode(payload).decode()

    signature = hmac.new(
        key=SK.encode(),
        msg=f'{b64_header}.{b64_payload}'.encode(),
        digestmod=hashlib.sha256
    ).digest()

    return f'Bearer {b64_header}.{b64_payload}.{base64.urlsafe_b64encode(signature).decode()}'


def validate_access_jwt( jwt ) -> dict:
    jwt_split = jwt.split(".")
    if len(jwt_split) != 3: abort(make_response("invalid token",401))

    b64_header, b64_payload, b64_signature = jwt_split

    signature_check = base64.urlsafe_b64encode(
        hmac.new(
            key = SK.encode(),
            msg=f'{b64_header}.{b64_payload}'.encode(),
            digestmod=hashlib.sha256
        ).digest()
    ).decode()

    payload = json.loads(base64.urlsafe_b64decode(b64_payload))
    unix_time_now = datetime.datetime.now().timestamp()

    if payload.get("exp") and payload["exp"] < unix_time_now: abort(make_response("token expired",401))
    
    if b64_signature != signature_check: abort(make_response("invalid token",401))

    
    return payload
