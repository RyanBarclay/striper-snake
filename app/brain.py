import math
import json
import numpy as np

debug = True
# global_temp_int_1 = 0
# global_temp_int_2 = 0 

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
                elif i == cur_snake_body_length-1:
                    if turn == 0:
                        board_matrix[cur_snake_body_y][cur_snake_body_x] ='mh'
                    else:
                        board_matrix[cur_snake_body_y][cur_snake_body_x] ='mt'
                else:
                    board_matrix[cur_snake_body_y][cur_snake_body_x] ='mb'
            else:
                if i == 0:
                    board_matrix[cur_snake_body_y][cur_snake_body_x] ='h'
                elif i == cur_snake_body_length-1:
                    if turn == 0:
                        board_matrix[cur_snake_body_y][cur_snake_body_x] ='h'
                    else:
                        board_matrix[cur_snake_body_y][cur_snake_body_x] ='t'
                else:
                    board_matrix[cur_snake_body_y][cur_snake_body_x] ='b'
            i += 1
        board_snakes_amount -= 1
    #end of look funtion

def instincts(board_matrix):

    # will find my head and tell me where it is and exit x,y
    head_pos_x = 0
    head_pos_y = 0
    element = 'mh'
    find_element_index_2d(board_matrix, element, head_pos_x,head_pos_y)
    print head_pos_x
    print head_pos_y

    choice= ['up','down','left','right']


    return choice[0]

def find_element_index_2d(matrix,element,x_input,y_input):
    y = len(matrix) - 1
    temp_token = matrix[0]
    x = len(temp_token) - 1
    end = False
    while y >= 0:
        while x >= 0:
            temp_element = matrix[y][x]
            if temp_element == element:
                end = True
            if end == True:
                break
            x -= 1
        if end == True:
            #when it finds head location do this
            x_input = x
            y_input = y
            break
        x= len(temp_token) - 1
        y -= 1

    if debug == True:
        if y == -1:
            print "ERROR element not found in find_element_index_2d"
        else:
            print "find_element_index_2d Working"
            print "x:%d y:%d"%(x,y)
