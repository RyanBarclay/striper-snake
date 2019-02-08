import math
import json
import numpy as np

debug = True


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
    # print board_food[0:2]
    board_snakes = board['snakes']  #Array of object (Snake)
    # print board_snakes

    you_id = you['id']
    you_name = you['name']
    you_health = you['health']
    you_body = you['body']

    board_matrix = [[0 for x in range(board_width)] for y in range(board_height)]
    # this will make an array elements of widths. ie
    look(board_food, board_snakes, you_id, board_matrix, turn)
    if debug == True:
        print(np.matrix(board_matrix))
    direction = instincts(board_matrix)
    return direction

def look(board_food, board_snakes, you_id, board_matrix, turn):

    """
    WHAT DIS DO:

    This funtion is to take the array of x,y postions of food and the snakes at
    positions in their array and 'simulate' the board for easy calculations

    *   will put 'f' in array where there is a food pellet
    *   will put 'h' if head of snake
    *   will put 't' if tale of snake
    *   will put 'b' if body of snake
    *   will put '0' if empty space
    """

    # we are going to do the food first
    food_amount = len(board_food)
    # print food_amount
    while food_amount > 0:
        food_token = board_food[food_amount-1]
        food_x = food_token['x']
        food_y = food_token['y']
        # print food_x
        # print food_y
        # board_matrix[height index][width index]
        board_matrix[food_y][food_x] = 'f'
        food_amount -= 1

    # now to do the snakes on board
    board_snakes_amount = len(board_snakes)
    # print board_snakes_amount

    while board_snakes_amount > 0:
        cur_snake = board_snakes[board_snakes_amount-1]
        cur_snake_id = cur_snake['id']
        cur_snake_body = cur_snake['body']
        cur_snake_body_length = len(cur_snake_body)
        # recond snake on array
        i = 0
        while i < cur_snake_body_length:
            cur_snake_body_token = cur_snake_body[i]
            cur_snake_body_x = cur_snake_body_token['x']
            cur_snake_body_y = cur_snake_body_token['y']
            if cur_snake_id == you_id:
                if i == 0:
                    board_matrix[cur_snake_body_y][cur_snake_body_x] ='mh'
                elif i== cur_snake_body_length-1:
                    if turn == 0:
                        board_matrix[cur_snake_body_y][cur_snake_body_x] ='mh'
                    elif turn == 1:
                        board_matrix[cur_snake_body_y][cur_snake_body_x] ='mt'
                    else:
                        board_matrix[cur_snake_body_y][cur_snake_body_x] ='mb'
                else:
                    board_matrix[cur_snake_body_y][cur_snake_body_x] ='mt'
            else:
                if i == 0:
                    board_matrix[cur_snake_body_y][cur_snake_body_x] ='h'
                elif i== cur_snake_body_length-1:
                    board_matrix[cur_snake_body_y][cur_snake_body_x] ='b'
                else:
                    board_matrix[cur_snake_body_y][cur_snake_body_x] ='t'
            i += 1
        board_snakes_amount -= 1
    #end of look funtion

def instincts(board_matrix):

    # will find my head and tell me where it is and exit x,y
    x,y = 0,0
    element = 'mh'
    find_element_index_2d(board_matrix,element,x,y)

    choice= ['up','down','left','right']

    if debug == True:
        if x == -1:
            print "find_element_index_2d failed"

    return choice[0]

def find_element_index_2d(matrix,element,x,y):
    x= len(matrix) - 1
    temp_token = matrix[0]
    y= len(temp_token) - 1
    end = False
    while x >= 0:
        while y >= 0:
            if matrix[y][x]== element:
                end = True
            else:
                y -= 1
        if end:
            break
        else:
            x -= 1
