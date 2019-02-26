import math
import json
#to make this work on heroku you must search for all instances of "*HEROKU_REMOVE*" and comment the line under them

#*HEROKU_REMOVE*
import numpy as np

debug = True

def think(data, inLoop, foodTrapped):
    """
    Function: think(data)

    Description:
        This function is the primary function of this file. It's directive, is to itemize all of the json data passed through the input. Then pass on the necessary data for each function.

        The functions will need to find out if its the closest to that food compared to other snakes, decide if it wants to go for the food, will make a 'closed box' around that food, when it is going to die will eat food, make a holding pattern 'closed box', then repeat.

    Input:
        data:
            This is a json payload with with the api looking like:
                {
                  "game": {
                    "id": "game-id-string"
                  },
                  "turn": 4,
                  "board": {
                    "height": 15,
                    "width": 15,
                    "food": [
                      {
                        "x": 1,
                        "y": 3
                      }
                    ],
                    "snakes": [
                      {
                        "id": "snake-id-string",
                        "name": "Sneky Snek",
                        "health": 90,
                        "body": [
                          {
                            "x": 1,
                            "y": 3
                          }
                        ]
                      }
                    ]
                  },
                  "you": {
                    "id": "snake-id-string",
                    "name": "Sneky Snek",
                    "health": 90,
                    "body": [
                      {
                        "x": 1,
                        "y": 3
                      }
                    ]
                  }
                }
        inLoop:
            Boolian value that will be true when snake in a type of loop

        foodTrapped:
            Boolian value that will be true when snake trapping food
    Output:
        direction:
            This will be  a string of 'up', 'down', 'left', or 'right'

        inLoop:
            Boolian value will be set to true when snake in a loop

        foodTrapped:
            Boolian value will be set to true when snake trapped food
    """
    # process data
    game = data['game']
    turn = data['turn']
    board = data['board']
    you = data['you']


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

    if debug:
        print("\nname: %s" % (you_name))
        print("\nturn: %s" % (turn))
        print("-------------------")

    board_matrix = [[0 for x in range(board_width)] for y in range(board_height)]
    # this will make an array elements of widths. ie

    look(board_food, board_snakes, you_id, board_matrix, turn)
    head_xy = head_finder(board_matrix)
    #initialize board representation and find my head

    food_location, closest = food_finder(board_food, you_id, board_snakes)
    #look for closest food and look if your the closest

    safe_moves = move_check(head_xy, board_matrix, turn)
    #finds acceptiable moves


    if inLoop is True:
        #if in loop/holding pattern do this
        if foodTrapped is True:
            #if in a loop and has already trapped food
            pass
        else:
            #if in loop and has already eaten food
            pass
    else:
        #if not in loop/holding patern go and get food
        pass
    #end of logic tree

    """
    TODO: remove the code below that is in this else fragment
    """

    moves, box = go_to_food(safe_moves, food_location, head_xy)
    if len(moves) == 0:
        choice = 'up'
    else:
        choice = moves[0]

    #debug print out
    if debug is True:
        print("\nthink DEBUG:")
        print("-------------------")
        print("think retuns returns:")
        print("choice: %s" % (choice) )
        print("-------------------")

    return choice, inLoop, foodTrapped

def look(board_food, board_snakes, you_id, board_matrix, turn):
    """
    Function:
        look()
    Description:
        This function is to take the array of x,y postions of food and the snakes at positions in their array and 'simulate' the board for easy calculations

        *   will put 'f' in array where there is a food pellet
        *   will put 'h' if head of snake
        *   will put 't' if tale of snake
        *   will put 'b' if body of snake
        *   will put '0' if empty space
    Input:
        board_food:
            list of { {[x: #][y: #]}, ...}

        board_snakes:
            reffer to think(date) explanation

        you_id:
            this is a string that identifies my snake

        board_matrix:
            this is an list of lists that represents the current board of Battle snake

        turn:
            this is an int that represents the turn in the game

    Output:
        alters board_matrix with current data

    """

    # we are going to do the food first
    food_amount = len(board_food)
    # print food_amount
    while food_amount > 0:
        food_token = board_food[food_amount-1]
        food_x = food_token['x']
        food_y = food_token['y']
        # board_matrix[height index][width index]
        board_matrix[food_y][food_x] = 'f'
        food_amount -= 1

    # now to do the snakes on board
    board_snakes_amount = len(board_snakes)

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
    if debug is True:
        print("\nlook DEBUG:")
        print("-------------------")
        #debug print out
        print("look edits:")
        print("board_matrix:")

        #use this when you want debug but are on heroku
        # print(board_matrix)

        #*HEROKU_REMOVE*
        print(np.matrix(board_matrix))

        print("-------------------")

def move_check(head_xy, board_matrix, turn):
    """
    Function:
        move_check()
    Description:
        will find what are outputs for move that won't instantly kill the snake
    Input:
        head_xy:
            This is a list containing two elements: x,y. These coords are the location of your head in the board matrix

        board_matrix:
            This is an list of lists that represents the current board of Battle snake

        turn:
            an int that represents the current turn
    Output:
        safe_choices:
            This is an list of moves that won't imediatlty kill the board_snakes
                ***IF THIS IS EMPTY****
                snake is dead because there are no safe moves

    """

    head_pos_x = head_xy[0]
    head_pos_y = head_xy[1]

    safe_choices = []

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

    if turn != 1:
        danger_elements.remove('mt')
        #removes base cases

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

    if debug is True:
        print("\nmove_check DEBUG:")
        print("-------------------")
        #debug print out
        print("move_check returns:")
        print("safe_choices: %s" % (safe_choices) )
        print("-------------------")

    return safe_choices

def food_finder(board_food, you_id, board_snakes):
    """
    This function should return food Coords in a list = [x,y] this food will be the food that gives the  value to the following formula:
    this works because the value with

    if no food on board then will return empty list and a flase on the boolian

    Input:
        board_food:
            list of { {[x: #][y: #]}, ...}
        you_id:
            id of my snake as a string
        board_snakes:
            reffer to think(date) explanation
    """
    food_index = len(board_food) - 1
    closest_in_comparison = False
    closest_food = []
    distance_list = []
    #this is a list of {[mysnake_distance, closest_snake_distnace]} elements
    padding =  2
    #VERY IMPORTANT
    #This controls how scared it is

    if len(board_food) == 0:
        # if no food
        return closest_food, closest_in_comparison

    while food_index >= 0:
        #cycle through food
        food_token = board_food[food_index]
        food_x = food_token['x']
        food_y = food_token['y']
        element = [0,0]
        #initializes elements to be loaded into distance_list

        snake_index = len(board_snakes) - 1
        while snake_index >= 0:
            snake_token = board_snakes[snake_index]
            cur_snake_body = snake_token['body']
            cur_snake_body_token = cur_snake_body[0]
            #cur_snake_body_token = head

            cur_snake_head_x = cur_snake_body_token['x']
            cur_snake_head_y = cur_snake_body_token['y']
            cur_snake_id = snake_token['id']

            delta_x = abs(food_x - cur_snake_head_x)
            delta_y = abs(food_y - cur_snake_head_y)
            diffrence = delta_x + delta_y

            if cur_snake_id  == you_id:
                #if my snake will put in how far it is from the food
                element[0] = diffrence

            else:
                #else find closest ememy snake to food
                if element[1] == 0:
                    #if first enemy snake it by deff is the closest ememy
                    element[1] = diffrence

                if element[1] > diffrence:
                    #if the this enemy snake is closer than the current closest one, replace it
                    element[1] = diffrence
            snake_index -= 1
        distance_list.insert(0,element)
        # distance_list.append(element)
        food_index -= 1
    # now there is a list of lists with my distance to food and the closest enemy to the food as elements
    distance_list_index = len(distance_list)-1

    while distance_list_index >= 0:
        #this will find the largest x value as stated above
        token = distance_list[distance_list_index]
        mysnake_distance = token[0]
        enemy_distance = token[1]
        # print("mysnake_distance: %s" % (mysnake_distance))
        # print("ememy_distance: %s" % (enemy_distance))
        if (mysnake_distance+ padding) < enemy_distance:
            #I am the closest to this food compared to the closest enemy to this food
            closest_in_comparison = True
            closest_food = board_food[distance_list_index]
            if debug:
                print("\nfood_finder DEBUG:")
                print("-------------------")
                print("This is the list distance_list:")
                print(distance_list)
                print("This is the board_food")
                print(board_food)
                print("This is the return entries of food_finder:")
                print("closest_food: %s" % (closest_food))
                print("closest_in_comparison: %s" % (closest_in_comparison))
                print("-------------------")
            return closest_food, closest_in_comparison
        else:
            #I'm not the closest to the food, so find closest food
            if distance_list_index == (len(distance_list)-1):
                #first time in loop
                smallest_distance = distance_list[0]
                closest_food = board_food[distance_list_index]
            else:
                if smallest_distance > distance_list[0]:
                    smallest_distance = distance_list[0]
                    closest_food = board_food[distance_list_index]
        distance_list_index -= 1
    if debug:
        print("\nfood_finder DEBUG:")
        print("-------------------")
        print("This is the list distance_list:")
        print(distance_list)
        print("This is the board_food")
        print(board_food)
        print("This is the return entries of food_finder:")
        print("closest_food: %s" % (closest_food))
        print("closest_in_comparison: %s" % (closest_in_comparison))
        print("-------------------")
    return closest_food, closest_in_comparison

def head_finder(board_matrix):
    """
    Function:
        head_finder()
    Description:
        this will find the head of your snake
    Input:
        board_matrix:
            this is an list of lists that represents the current board of Battle snake
    Output:
        head_xy:
            this is a list containing two elements: x,y. These coords are the location of your head in the board matrix

    """
    head_pos_y = len(board_matrix)-1
    head_token = board_matrix[0]
    head_pos_x = len(head_token)-1
    x_max = head_pos_x
    head_indicator = 'mh'
    end = False

    while head_pos_y >= 0:
        while head_pos_x >= 0:
            if board_matrix[head_pos_y][head_pos_x] == head_indicator:
                end = True
                break
            else:
                head_pos_x -= 1
        if end is True:
            break
        else:
            head_pos_y -= 1
            head_pos_x = x_max
    head_xy = [head_pos_x, head_pos_y]

    if debug is True:
        print("\nhead_finder DEBUG:")
        print("-------------------")
        #debug print out
        print("head_finder returns:")
        print("head_xy: %s" % (head_xy) )
        print("-------------------")

    return head_xy

def go_to_food(safe_choices, food_location, head_xy):
    """
    Function:
        go_to_food()

    Description:
        this will go make the snake go to food and tell us if the snake is ready to make a 'box' around food

        Algorithm:
            1.is the head within box of food?
                a. if so return move as empty, return True to ready_to_box boolian

                b   else go to 2

            2.is snake diagnal with food?
                a.  if so return a move up or down will get it closer to food and false to the ready_to_box boolian

                b.  else go to 1

            3.return a move that wont kill it and will try and bring it closer to diagnal go diagnal. if it is going to die will go up.
                -8  possible outcomes for going to closest diagnal. reffer to documentation folder for area numbers and logic

    Input:
        safe_choices:
            This is an list of moves that won't imediatlty kill the snake.
                ***IF THIS IS EMPTY****
                snake is dead because there are no safe moves.

        food_location:
            a list comprised of { {[x: #][y: #]}} that is the location food it wants to get

        head_xy:
            This is a list containing two elements: x,y. These coords are the location of your head in the board matrix.

    Output:
        move:
            this will be move that it picks in a string format.
                ***IF EMPTY***
                ready to protect food.

        ready_to_box:
            this is a boolian that will tell us if the snake is ready to go from going to food to protecting food

    """
    #process input
    head_pos_x = head_xy[0]
    head_pos_y = head_xy[1]

    #establish local varibles
    move = []
    ready_to_box = False
    diagnal = False
    inSquare = False
    food_x = food_location['x']
    food_y = food_location['y']
    areaNumber = 0

    delta_x = head_pos_x - food_x
    delta_y = food_y - head_pos_y

    # start of logic

    #1 logic
    if abs(delta_x) is 1:
        if abs(delta_y) is 1:
            #head is in a corner of square surrounding food
            inSquare = True
        elif abs(delta_y) is 0 :
            #head to the left or right of food
            inSquare = True
    if abs(delta_y) is 1:
        if abs(delta_x) is 0:
            inSquare = True
            #head is above or below food

    #2 logic
    if delta_y == delta_x:
        #is diagnal either top Q1 or Q3
        diagnal = True
    elif -delta_y == delta_x:
        #is diagnal either top Q2 or Q4
        diagnal = True

    if delta_y > 0:
        #if in  q1 or q2 goes down
        move.append('down')
    else:
        #if in q3 or q4 goes up
        move.append('up')

    #logic tree
    if inSquare:
        #1a
        move = []
        ready_to_box = True
        #debug print out
        if debug is True:
            print("\ngo_to_food DEBUG:")
            print("-------------------")
            print("go_to_food returns:")
            print("move: %s" % (move))
            print("ready_to_box: %s" % (ready_to_box))
            print("-------------------")
        return move, ready_to_box
    elif diagnal:
        #2a
        ready_to_box = False
        #debug print out
        if debug is True:
            print("\ngo_to_food DEBUG:")
            print("-------------------")
            print("go_to_food returns:")
            print("move: %s" % (move))
            print("ready_to_box: %s" % (ready_to_box))
            print("-------------------")
        return move, ready_to_box
        pass
    else:
        """
        TODO:
        Fix how it realigns to diagnal and goes to diagnal
        """
        #3
        #make snake move closer to the diagnal and avoid obsticles
        move = []
        ready_to_box =  False
        print("This is the 3rd case")
        print("delta_y: %s" % (delta_y))
        print("delta_x: %s" % (delta_x))

        if delta_y >= 0:
            #top half of cases
            if delta_x >= 0:
                if abs(delta_x) < abs(delta_y):
                    #2
                    areaNumber = 2
                    move.append('down')
                else:
                    #1
                    areaNumber = 1
                    move.append('left')
            else:
                if abs(delta_x) < abs(delta_y):
                    #3
                    areaNumber = 3
                    move.append('down')
                else:
                    #4
                    areaNumber = 4
                    move.append('right')
        else:
            if delta_x >= 0:
                if abs(delta_x) < abs(delta_y):
                    #7
                    areaNumber = 7
                    move.append('up')
                else:
                    #8
                    areaNumber = 8
                    move.append('left')
            else:
                if abs(delta_x) < abs(delta_y):
                    #6
                    areaNumber = 6
                    move.append('up')
                else:
                    #5
                    areaNumber = 5
                    move.append('right')
        #move will be equal to what it should be returning in a prefect world
        move_element = move[0]
        if move_element in safe_choices:
            #debug print out
            if debug is True:
                print("\ngo_to_food DEBUG:")
                print("-------------------")
                print("go_to_food returns:")
                print("move: %s" % (move))
                print("ready_to_box: %s" % (ready_to_box))
                print("area: %s" % (areaNumber))
                print("-------------------")
            return move,ready_to_box
        else:
            move = []
            if len(safe_choices) is 0:
                move.append('up')
                #were dead
            else:
                move_element = safe_choices[0]
                move.append(move_element)
            #debug print out
            if debug is True:
                print("\ngo_to_food DEBUG:")
                print("-------------------")
                print("go_to_food returns:")
                print("move: %s" % (move))
                print("ready_to_box: %s" % (ready_to_box))
                print("area: %s" % (areaNumber))
                print("-------------------")
            return move,ready_to_box
