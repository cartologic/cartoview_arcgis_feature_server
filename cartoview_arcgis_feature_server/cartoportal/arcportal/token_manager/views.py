__author__ = 'Ahmed Nour eldeen'

import uuid
import binascii
import base64
import hashlib
import time
from models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()

from ..json_response_utils import JsonResponse, JsonPResponse

# token validation period in milliseconds
TOKEN_VALIDATION_PERIOD = 24 * 60 * 60 * 1000


@csrf_exempt
def generate_token(request):
    token_json = {}
    if 'username' in request.REQUEST:
        user = User.objects.get(username__exact=request.REQUEST['username'])
        if user.check_password(request.REQUEST['password']):
            token_obj = Token.objects.create(user=user, token=get_token(user), expiration_date=get_expiration_date())
            token_obj.save()
            token_json = {
                "token": token_obj.token,
                "expires": token_obj.expiration_date,
                "ssl": False
            }
        else:
            token_json = {"error": {
                "code": 400,
                "message": "Unable to generate token.",
                "details": ["'username' must be specified.",
                            "'password' must be specified.",
                            "'referer' must be specified."]
            }}
    else:
        token_json = {"error": {
            "code": 400,
            "message": "Unable to generate token.",
            "details": ["'username' must be specified.",
                        "'password' must be specified.",
                        "'referer' must be specified."]
        }}
    print token_json
    if 'callback' in request.REQUEST:
        return JsonPResponse(content=token_json, callback=request.REQUEST["callback"])
    else:
        return JsonResponse(content=token_json)


def get_token(user):
    # TODO: salt must be generated randomly.
    # return binascii.b2a_base64(hashlib.pbkdf2_hmac('sha1', user.username, b'salt', 1000)).rstrip() + str(uuid.uuid4())
    #### Updated by Mohamed Gamal because pbkdf2_hmac is not allowed in python 7.2.2
    return base64.b64encode(hashlib.sha1(user.username).digest()) + str(uuid.uuid4())


def is_valid_token(token):
    try:
        return Token.objects.get(token=token).expiration_date > time.time()
    except:
        return False


def validate_token(request):
    if 'token' in request.REQUEST:
        if is_valid_token(request.REQUEST['token']):
            return True
    else:
        return True


def get_expiration_date():
    return time.time() * 1000 + TOKEN_VALIDATION_PERIOD
