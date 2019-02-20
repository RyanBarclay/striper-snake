import json
from bottle import HTTPResponse

def ping_response():
    return HTTPResponse(
        status=200
    )

def start_response(color):
    # def start_response(color, headType, tailType):
    assert type(color) is str, \
        "Color value must be string"

    # assert type(headType) is str, \
    #     'headType value must be "beluga" "bendr" "dead" "evil" "fang" "pixel" "regular" "safe" "sand-worm" "shades" "silly" "smile" "tongue"'

    # assert type(tailType) is str, \
    #     'tailType valuse must be "block-bum" "bolt" "curled" "fat-rattle" "freckled" "hook" "pixel" "regular" "round-bum" "sharp" "skinny" "small-rattle"'

    return HTTPResponse(
        status=200,
        headers={
            "Content-Type": "application/json"
        },
        body=json.dumps({
            "color": color
            # "headType": headType,
            # "tailType": tailType

        })
    )

def move_response(move):
    assert move in ['up', 'down', 'left', 'right'], \
        "Move must be one of [up, down, left, right]"

    return HTTPResponse(
        status=200,
        headers={
            "Content-Type": "application/json"
        },
        body=json.dumps({
            "move": move
        })
    )

def end_response():
    return HTTPResponse(
        status=200
    )
