import math
import json
# import numpy as np

debug = False

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
    direction = instincts(board_matrix, board_food)
    if debug == True:
        # print(np.matrix(board_matrix))
        print("think debug")
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

def instincts(board_matrix, board_food):

    # will find my head and tell me where it is and exit x,y
    head_pos_y = len(board_matrix)-1
    head_token = board_matrix[0]
    head_pos_x = len(head_token)-1
    x_max = head_pos_x
    element = 'mh'
    end = False
    safe_choices = []

    # this finds the head .... hopefully no bugs
    while head_pos_y >= 0:
        while head_pos_x >= 0:
            if board_matrix[head_pos_y][head_pos_x] == element:
                end = True
                break
            else:
                head_pos_x -= 1
        if end == True:
            break
        else:
            head_pos_y -= 1
            head_pos_x = x_max
    # end of find head loop

    if debug == True:
        print "head of snake x:%d ,y:%d" %(head_pos_x,head_pos_y)

    safe_choices = move_check(safe_choices, head_pos_x, head_pos_y, board_matrix)


    return hunting(safe_choices, board_food,head_pos_x,head_pos_y)

def move_check(safe_choices, head_pos_x, head_pos_y, board_matrix):
    """
    This will return a pool of moves that are acceptable as moves and return it
    as a list of those moves as strings acceptable as /move entries
    """

    temp_token = board_matrix[0]

    top_edge = 0
    right_edge = len(temp_token)-1
    left_edge = 0
    bottom_edge = len(board_matrix)-1

    up_clear = True
    down_clear = True
    left_clear = True
    right_clear = True

    danger_elements = ['h','b','mb','t','mt']


    #if up is a bad move, remove it as an option
    if head_pos_y == top_edge:
        up_clear = False
    else:
        up_element = board_matrix[head_pos_y-1][head_pos_x]
        if up_element in danger_elements:
            up_clear = False

    #if down is a bad move, remove it as an option
    if head_pos_y == bottom_edge:
        down_clear = False
    else:
        down_element = board_matrix[head_pos_y+1][head_pos_x]
        if down_element in danger_elements:
            down_clear = False

    #if left is a bad move, remove it as an option
    if head_pos_x == left_edge:
        left_clear = False
    else:
        left_element = board_matrix[head_pos_y][head_pos_x-1]
        if left_element in danger_elements:
            left_clear = False

    #if right is a bad move, remove it as an option
    if head_pos_x == right_edge:
        right_clear = False
    else:
        right_element = board_matrix[head_pos_y][head_pos_x+1]
        if right_element in danger_elements:
            right_clear = False

    #now to update the list of safe moves
    if up_clear:
        safe_choices.append('up')

    if down_clear:
        safe_choices.append('down')

    if left_clear:
        safe_choices.append('left')

    if right_clear:
        safe_choices.append('right')

    return safe_choices

def hunting(safe_choices, board_food,head_pos_x,head_pos_y):
    food_location = food_finder(board_food,head_pos_x,head_pos_y)
    if len(food_location) == 0:
        food_x = 0
        food_y=0
    else:
        food_x = food_location[0]
        food_y = food_location[1]
    if debug:
        # print np.matrix(safe_choices)
        print("Hunting degug")

    if head_pos_x != food_x:
        if (head_pos_x > food_x):
            #if head_pos_x is > food, head is to the right of food
            if 'left' in safe_choices:
                return 'left'
            else:
                #check y alignment and see if thats a move otherwise do first
                #element in safe_choices
                #this is when it right above food
                if head_pos_y > food_y:
                    #if head > food_y, go up check
                    if 'up' in safe_choices:
                        return 'up'
                    else:
                        return safe_choices[0]
                else:
                    #if head < food_y, go down check
                    if 'down' in safe_choices:
                        return 'down'
                    else:
                        return safe_choices[0]
        else:
            #if head_pos_x is < food, head is to the right of food
            if 'right' in safe_choices:
                return 'right'
            else:
                #check y alignment and see if thats a move otherwise do first
                #element in safe_choices
                #this is when it right above food
                if head_pos_y > food_y:
                    #if head > food_y, go up check
                    if 'up' in safe_choices:
                        return 'up'
                    else:
                        return safe_choices[0]
                else:
                    #if head < food_y, go down check
                    if 'down' in safe_choices:
                        return 'down'
                    else:
                        return safe_choices[0]
    else:
        #this is when it right above food
        if head_pos_y > food_y:
            #if head > food_y, go up check
            if 'up' in safe_choices:
                return 'up'
            else:
                return safe_choices[0]
        else:
            #if head < food_y, go down check
            if 'down' in safe_choices:
                return 'down'
            else:
                return safe_choices[0]

def food_finder(board_food,head_pos_x,head_pos_y):
    """
    find the closest food in a list = [x,y]
    """
    food_amount = len(board_food)
    closest_food = []
    closest_distance = 0
    current_distance = 0
    x_delta = 0
    y_delta = 0

    if food_amount == 0:
        return closest_food

    while food_amount > 0:
        food_token = board_food[food_amount-1]
        food_x = food_token['x']
        food_y = food_token['y']
        x_delta = food_x - head_pos_x
        x_delta = abs(x_delta)
        y_delta = food_y - head_pos_y
        y_delta = abs(y_delta)
        current_distance = y_delta + x_delta
        #print "current_distance: %d, closest_distance: %d" %(current_distance, closest_distance)
        if food_amount == len(board_food):
            #first time in loop
            closest_distance = current_distance

        if current_distance <= closest_distance:
            closest_food = [food_x,food_y]
            closest_distance = current_distance

        food_amount -= 1

    if debug:
            if len(closest_food) != 2:
                print "ERROR food_finder, food finder produced"
                # print (np.matrix(closest_food))
            else:
                print ("this is where the closest food is :")
                # print np.matrix(closest_food)
    return closest_food
