# -*- coding: utf-8 -*-

# pyramid entry point: semantic name
from __future__ import absolute_import

from ..router import router
from ..errors import DDBError, AccessDeniedException, MissingAuthenticationTokenException, InternalServerError
from ..config import config, config_for_user, FAIL_KEY, reset_fail
from ..utils import req_logger
from pyramid.response import Response
import json
from time import sleep

default_config = config["_default"]

# wrap routing logic
def pyramid_router(request):
    # extract action
    target = request.headers.get('x-amz-target')
    action = target.split('.', 2)[1] if target is not None else ""

    post = request.json

    # do the job
    try:
        auth = request.headers["Authorization"]
        if not auth.startswith("AWS4-HMAC-SHA256"):
            raise MissingAuthenticationTokenException
        auth = auth[len("AWS4-HMAC-SHA256 "):]
        auth = auth.split(", ")
        auth = dict([x.split("=",2) for x in auth])
        access_key = auth["Credential"].split("/")[0]
        if access_key not in config.keys():
            req_logger.error("Access denied for %s", access_key)
            raise AccessDeniedException, "Can't find %s in users" % access_key
        user = config_for_user(access_key)

        fail_every = user["FAIL_EVERY_N"]
        if fail_every != None and fail_every + 1 == user[FAIL_KEY]: # hit the fail time
            reset_fail(access_key)
            raise InternalServerError("The server encountered an internal error trying to fulfill the request")

        body = router(action, post, user)
        status = '200 OK'
    except DDBError as e:
        body = e.to_dict()
        status = '{} {}'.format(e.status, e.status_str)
        user = None

    # prepare output
    response = Response()
    response.body = json.dumps(body)
    response.status = status
    response.content_type = 'application/x-amz-json-1.0'
    if post.has_key("request_id"): # might not be present if user auth failed
        response.headers['x-amzn-RequestId'] = post['request_id']  # added by router

    if user != None:
        sleep(user["DELAY_OPERATIONS"])

    # done
    return response
