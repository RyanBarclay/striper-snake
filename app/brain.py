import math
import json


def think(data):
    #this is where the work starts
    # just to make this snake not die we need it to just be able to play snake
    game = data['game']
    turn = data['turn']
    board = data['board']
    you = data['you']

    # process data
    game_id = game['id']

    board_height = board['height']
    board_width = board['width']
    board_food = board['food']      #Array of object (Coords)
    board_snakes = board['snakes']  #Array of object (Snake)

    you_id = you['id']
    you_name = you['name']
    you_health = you['health']
    you_body = you['body']

    return 'up'
