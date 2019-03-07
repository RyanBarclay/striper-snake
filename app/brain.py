import math
import json
#To make this work on heroku you must search for all instances of "*HEROKU_REMOVE*" and comment the line under them

#*HEROKU_REMOVE*
# import numpy as np

debug = False

def think(data, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready):
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

        spawn_xy:
            This is a list containing two elements: x,y. These coords are the location of your head when you started game in the board matrix

        move_history:
            This is a list containing all of my moves this game. The elements of this list are 'up', 'down', 'left', or 'right'. The most recent move is placed in the begining of this list.

        tail_loop_ready:
            Boolian value that will be true snake is in the middle of making a tail loop


    Output:
        direction:
            This will be  a string of 'up', 'down', 'left', or 'right'

        inLoop:
            Boolian value will be set to true when snake in a loop

        foodTrapped:
            Boolian value will be set to true when snake trapped food

        spawn_xy:
            this is a list containing two elements: x,y. These coords are the location of your head when you started game in the board matrix
    """
    #Process data
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
    you_length = len(you_body)

    if debug:
        print("\nname: %s" % (you_name))
        print("snake_id: %s" % (you_id))
        print("turn: %s" % (turn))
        print("tail_loop_ready: %s" % (tail_loop_ready))
        print("inLoop: %s" % (inLoop))
        print("foodTrapped: %s" % (foodTrapped))

        print("-------------------")

    board_matrix = [[0 for x in range(board_width)] for y in range(board_height)]
    #This will make an array elements of widths. ie

    look(board_food, board_snakes, you_id, board_matrix, turn)
    head_xy = head_finder(board_matrix)
    #Initialize board representation and find my head
    move_history_initalize = []
    if turn is 0:
        spawn_xy = head_xy
        move_history = move_history_initalize

    food_location, closest = food_finder(board_food, you_id, board_snakes)
    #Look for closest food and look if your the closest

    safe_choices = move_check(head_xy, board_matrix, turn)
    #Finds acceptiable moves

    """EDIT MAIN VALUES"""
    hungerThreshold = 40

    choice = 'up'
    #initializes the outputs

    adolescence = [3,4]
    if you_length in adolescence:
        young = True
    else:
        young = False

    if inLoop is True:
        #If in loop/holding pattern do this
        if foodTrapped is True:
            #If in a loop and has already trapped food
            #Check if it wants to eat food yet based off of health
            #Eats food starts to happen if health threshhold is met

            #checkIfNeedToEat
                #yes
                #eatFoodInLoop function
                #no
                #stayInLoop function
            if you_health < hungerThreshold-16:
                pass
                #eatFoodInLoop()
                #10
            else:
                choice = stay_in_loop()
                """REMOVE"""
                move_history.insert(0,choice)
                return choice, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready
                """END-OF-REMOVE"""
                #9
        else:
            #If in loop and has already eaten food or is young
            #Snake should stay in the loop untill it can get food and it knows it can

            #Logic

            #checkIfNeedToEat, this needs to check if no food (if so no is ans)
                #yes
                #goEatFood funtion,  inloop = false
                #no
                #if safe to go to food
                    #yes
                    #go_to_food, inloop = false
                    #no
                    #Stayinloop function

            if you_health < hungerThreshold:
                choice = eat_food(head_xy, food_location, safe_choices)
                inLoop = False

                """REMOVE"""
                move_history.insert(0,choice)
                return choice, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready
                """END-OF-REMOVE"""
                #7a
            else:
                if closest is True:
                    moves, box_ready = go_to_food(safe_choices, food_location, head_xy)
                    choice = moves[0]
                    inLoop = False
                    foodTrapped = False
                    """REMOVE"""
                    move_history.insert(0,choice)
                    return choice, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready
                    """END-OF-REMOVE"""
                    #8
                else:
                    choice = stay_in_loop()
                    """REMOVE"""
                    move_history.insert(0,choice)
                    return choice, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready
                    """END-OF-REMOVE"""
                    #7
                    pass
    else:
        #If not in loop/holding patern do this
        if young is True:
            #too young to make a food loop so it will
            # 1. Is it the start(first 4 moves), if so loop with its self
            # 2. Check if closest for food. if so will go and eat food
            # 3. Make a loop with its self
            if(turn <= 2):
                #is it in the first 3 moves
                choice = makeFirstLoop(inLoop, safe_choices, turn, spawn_xy, board_matrix)
                """REMOVE"""
                move_history.insert(0,choice)
                return choice, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready
                """END-OF-REMOVE"""
                #6
                #DONE
            else:
                if(you_health < (hungerThreshold + 20)):
                    choice = eat_food(head_xy, food_location, safe_choices)
                else:
                    if closest is True:
                        #2
                        choice = eat_food(head_xy, food_location, safe_choices)
                        """REMOVE"""
                        move_history.insert(0,choice)
                        return choice, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready
                        """END-OF-REMOVE"""
                        #5
                    else:
                        #3
                        choice, inLoop = make_young_loop(you_length, head_xy, board_matrix, move_history, safe_choices)
                        """REMOVE"""
                        move_history.insert(0,choice)
                        return choice, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready
                        """END-OF-REMOVE"""
                        #4

        else:
            #Go and get food because it has already decided
            moves, box_ready = go_to_food(safe_choices, food_location, head_xy)
            if box_ready is True:
                #ignore move and start making a loop
                     #if this makes a loop makes inLoop true
                choice, tail_loop_ready, inLoop, foodTrapped =  make_head_box(board_matrix, food_location, you_length, head_xy, tail_loop_ready, inLoop, foodTrapped)
                if tail_loop_ready is True:
                    #make_tail_loop
                    pass
                    #3
                else:
                    choice, tail_loop_ready, inLoop, foodTrapped =  make_head_box(board_matrix, food_location, you_length, head_xy, tail_loop_ready, inLoop, foodTrapped)
                    pass
                    #2
                """REMOVE"""
                move_history.insert(0,choice)
                return choice, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready
                """END-OF-REMOVE"""
            else:
                #go to food or make tail loop
                #if need_to_make_tailloop == true
                    #continue tail loop funtion
                    #else go to food
                if tail_loop_ready is True:
                    choice = make_tail_loop()
                    #1
                else:
                    choice = moves[0]
                """REMOVE"""
                move_history.insert(0,choice)
                return choice, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready
                """END-OF-REMOVE"""
                #1
                pass
    #end of logic tree

    """
    KNOWN PROBLEMS:
        * When snake goes to get food and it is eaten for some reason it doesnt have know explicitly what to do
        * If a food spawns in the one/two spaces that it leaves to eat food it no explicit instance
    """

    """
    TODO: remove the code below that is in this if/else, go_to_food call fragment
    """

    moves, box = go_to_food(safe_choices, food_location, head_xy)
    if box:
        choice = eat_food(head_xy, food_location, safe_choices)
        #print("Temp return")
        #print(choice)
    else:
        choice = moves[0]

    #debug print out
    if debug is True:
        print("\nthink DEBUG:")
        print("-------------------")
        print("think retuns returns:")
        print("choice: %s" % (choice) )
        print("inLoop: %s" % (inLoop))
        print("foodTrapped: %s" % (foodTrapped))
        print("spawn_xy: %s" % (spawn_xy))
        print("-------------------")
    move_history.insert(0,choice)
    return choice, inLoop, foodTrapped, spawn_xy, move_history, tail_loop_ready

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
            This is an list of lists that represents the current board of Battle snake. Follows board_matrix[y][x]

        turn:
            this is an int that represents the turn in the game

    Output:
        N/A

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
        # print(np.matrix(board_matrix))

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
            This is an list of lists that represents the current board of Battle snake. Follows board_matrix[y][x].

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

    danger_elements = ['h','b','mb','t']

    #if up is a bad move, remove it as an option
    if head_pos_y == top_edge:
        up_clear = False
    else:
        up_element = board_matrix[head_pos_y-1][head_pos_x]
        if up_element in danger_elements:
            up_clear = False
        elif turn is 1:
            if up_element is 'mt':
                up_clear = False
    #if down is a bad move, remove it as an option
    if head_pos_y == bottom_edge:
        down_clear = False
    else:
        down_element = board_matrix[head_pos_y+1][head_pos_x]
        if down_element in danger_elements:
            down_clear = False
        elif turn is 1:
            if down_element is 'mt':
                down_clear = False

    #if left is a bad move, remove it as an option
    if head_pos_x == left_edge:
        left_clear = False
    else:
        left_element = board_matrix[head_pos_y][head_pos_x-1]
        if left_element in danger_elements:
            left_clear = False
        elif turn is 1:
            if left_element is 'mt':
                left_clear = False

    #if right is a bad move, remove it as an option
    if head_pos_x == right_edge:
        right_clear = False
    else:
        right_element = board_matrix[head_pos_y][head_pos_x+1]
        if right_element in danger_elements:
            right_clear = False
        elif turn is 1:
            if right_element is 'mt':
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

    #debug print out
    if debug is True:
        print("\nmove_check DEBUG:")
        print("-------------------")
        print("move_check returns:")
        print("safe_choices: %s" % (safe_choices) )
        print("-------------------")

    return safe_choices

def food_finder(board_food, you_id, board_snakes):
    """
    This function should return food Coords in a list = [x,y] this food will be the food that gives the  value to the following formula:
    this works because the value with

    if no food on board then will return [0,0] and a flase on the boolian

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
        closest_food = {'y': 0, 'x': 0}
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

    while food_index >= 0:
        #cycle through food
        food_token = board_food[food_index]
        food_x = food_token['x']
        food_y = food_token['y']
        element = [0,0,0]
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
        element[2] = food_index
        distance_list.append(element)
        # distance_list.append(element)
        food_index -= 1
    # now there is a list of lists with my distance to food and the closest enemy to the food as elements
    distance_list_index = len(distance_list)-1
    sorted = []
    while True:
        sorted_end = len(sorted) - 1
        if distance_list_index == sorted_end:
            #if I have passed all elements to the new list
            break
        #this will sort distance_list and put the greatest diffrence as last
        token = distance_list[0]
        #looks at first
        mysnake_distance = token[0]
        enemy_distance = token[1]
        diffrence = enemy_distance - mysnake_distance
        if sorted_end == -1:
            #base case
            greatest_diffrence = diffrence

        if greatest_diffrence <= diffrence:
            sorted.append(token)
            greatest_diffrence = diffrence
            del distance_list[0]

        else:
            sorted.insert(0,token)
            del distance_list[0]

    distance_list = sorted
    while distance_list_index >= 0:
        #this will find the largest x value as stated above
        token = distance_list[distance_list_index]
        mysnake_distance = token[0]
        enemy_distance = token[1]
        food_reffrence_index = token[2]
        # print("mysnake_distance: %s" % (mysnake_distance))
        # print("ememy_distance: %s" % (enemy_distance))
        if (mysnake_distance+ padding) < enemy_distance:
            #I am last element that is closer to the food plus padding
            closest_in_comparison = True
            closest_food = board_food[food_reffrence_index]
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
                closest_food = board_food[food_reffrence_index]
            else:
                if smallest_distance > distance_list[0]:
                    smallest_distance = distance_list[0]
                    closest_food = board_food[food_reffrence_index]
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
            This is an list of lists that represents the current board of Battle snake. Follows board_matrix[y][x]
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
        #move = make_head_box( )
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
        move_element = move[0]

        #dumb move check
        if move_element in safe_choices:
            #debug print out
            if debug is True:
                print("\ngo_to_food DEBUG:")
                print("-------------------")
                print("go_to_food returns:")
                print("move: %s" % (move))
                print("ready_to_box: %s" % (ready_to_box))
                print("-------------------")
            return move, ready_to_box
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
    else:
        #3
        #make snake move closer to the diagnal and avoid obsticles
        move = []
        ready_to_box =  False

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

def makeFirstLoop(inLoop, safe_choices, turn, spawn_xy, board_matrix):
    """
    Function:
        makeFirstLoop()
    Description:
        Will handle the the first 3 moves of the snake in order to make a loop that won't kill it in these moves

        There is only a problem when the board is 7x7 so this will be a basecase. The good news is that any bigger we can just do a basic loop
    Input:
        inLoop:
            Boolian value will be set to true when snake in a loop

        safe_choices:
            This is an list of moves that won't imediatlty kill the board_snakes
                ***IF THIS IS EMPTY****
                snake is dead because there are no safe moves

        turn:
            this is an int that represents the turn in the game

        spawn_xy:
            this is a list containing two elements: x,y. These coords are the location of your head when you started game in the board matrix

        board_matrix:
            This is an list of lists that represents the current board of Battle snake. Follows board_matrix[y][x]

    Output:
        choice:
            a string that is either 'up', 'down', 'right', 'left'
    """

    #find how big board is
    board_height = len(board_matrix)

    #edit choice
    if(board_height > 7):
        #if not 7x7 case do this
        if turn == 0:
            choice = 'up'
        elif turn == 1:
            choice = 'left'
        else:
            choice = 'down'
    else:
        #if 7x7 case

        #get my head
        my_spawn_x = spawn_xy[0]
        my_spawn_y = spawn_xy[1]

        #if in a corner starting pos will go control inLoop, if not it will just try and make a loop ... fingers crossed
        if my_spawn_x is 1:
            if my_spawn_y is 1:
                if turn == 0:
                    choice = 'up'
                elif turn == 1:
                    choice = 'left'
                else:
                    choice = 'down'
            elif my_spawn_y is 5:
                if turn == 0:
                    choice = 'left'
                elif turn == 1:
                    choice = 'down'
                else:
                    choice = 'right'
            else:
                if turn == 0:
                    choice = 'left'
                elif turn == 1:
                    choice = 'down'
                else:
                    choice = 'right'
        elif my_spawn_x is 5:
            if my_spawn_y is 1:
                if turn == 0:
                    choice = 'up'
                elif turn == 1:
                    choice = 'right'
                else:
                    choice = 'down'
            elif my_spawn_y is 5:
                if turn == 0:
                    choice = 'right'
                elif turn == 1:
                    choice = 'down'
                else:
                    choice = 'left'
            else:
                if turn == 0:
                    choice = 'right'
                elif turn == 1:
                    choice = 'up'
                else:
                    choice = 'left'
        else:
        #x = 3
            if my_spawn_y is 1:
                if turn == 0:
                    choice = 'up'
                elif turn == 1:
                    choice = 'left'
                else:
                    choice = 'down'
            else:
                if turn == 0:
                    choice = 'down'
                elif turn == 1:
                    choice = 'left'
                else:
                    choice = 'up'

    #check for danger
    if choice in safe_choices:
        choice = choice
        if turn == 2:
            inLoop = True
    else:
        choice = safe_choices[0]
        print("NOT IN SAFE")
        if turn == 3:
            inLoop = False
    #decided if in loop

    #debug print out
    if debug is True:
        print("\nmakeFirstLoop DEBUG:")
        print("-------------------")
        print("inLoop = %s" % (inLoop))
        print("makeFirstLoop returns:")
        print("choice: %s" % (choice) )
        print("-------------------")
    return choice

def eat_food(head_xy, food_location, safe_choices):
    """
    Function:
        eat_food()
    Description:
        This will go and eat the food asap
    Input:
        head_xy:
            This is a list containing two elements: x,y. These coords are the location of your head in the board matrix.

        food_location:
            a list comprised of { {[x: #][y: #]}} that is the location food it wants to get

        safe_choices:
            This is an list of moves that won't imediatlty kill the board_snakes
                ***IF THIS IS EMPTY****
                snake is dead because there are no safe moves
    Output:
        move:
            this is a list containing two elements: x,y. These coords are the location of your head in the board matrix

    """
    head_pos_x = head_xy[0]
    head_pos_y = head_xy[1]
    food_x = food_location['x']
    food_y = food_location['y']
    if head_pos_y < food_y:
        #if above or in top 2 corners go down
        move = 'down'
    elif head_pos_y > food_y:
        #if below or in bottom two corners do up
        move = 'up'
    elif head_pos_x > food_x:
        #if right go left
        move = 'left'
    elif head_pos_x < food_x:
        #if left go right
        move = 'right'

    if move in safe_choices:
        return move
    else:
        move = safe_choices[0]

        if debug is True:
            print("\neat_food DEBUG:")
            print("-------------------")
            #debug print out
            print("eat_food returns:")
            print("move: %s" % (move) )
            print("-------------------")

        return move

def make_young_loop(you_length, head_xy, board_matrix, move_history, safe_choices):
    """
    Function:
        make_young_loop()
    Description:
        This will make a loop when snake is length 3,4,5,6
    Input:
        you_length:
            length of my snake as an integer.

        head_xy:
            This is a list containing two elements: x,y. These coords are the location of your head in the board matrix.

        board_matrix:
            This is an list of lists that represents the current board of Battle snake. Follows board_matrix[y][x]

        move_history:
            This is a list containing all of my moves this game. The elements of this list are 'up', 'down', 'left', or 'right'. The most recent move is placed in the begining of this list.

        safe_choices:
            This is an list of moves that won't imediatlty kill the board_snakes
                ***IF THIS IS EMPTY****
                snake is dead because there are no safe moves
    Output:
        move:
            this is a list containing two elements: x,y. These coords are the location of your head in the board matrix

    """
    move = 'up'
    head_pos_x = head_xy[0]
    head_pos_y = head_xy[1]
    inLoop_check = False
    inLoop = False
    if you_length is 3:
        #3 turns
            #1 up
            #2 left/right
            #3 down
        #checks if it is already in a loop
        """TODO"""

        #if not in a loop do this
        #if #3 = 2nd done and 1st done
        #2 = if 1st is done
        #1 =  catch
        print("last move:")
        print(move_history[0])
        print(move_history)
        if (move_history[0] == 'left')or (move_history[0] == 'right'):
            #2 check
            #if it has done this then it may be done the second move
            if move_history[1] == 'up':
                #if has done #2 and #1 try and complete the loop with down
                move = 'down'
                inLoop_check = True
            else:
                #went left or right (#2) last turn but it wasnt a loop move
                #will try up
                move = 'up'
        else:
            #at most done step #1
            if move_history[0] == 'up':
                print("here")
                if 'left' in safe_choices:
                    move = 'left'
                if 'right' in safe_choices:
                    move = 'right'
            else:
                #no steps done
                move = 'up'

    elif you_length is 4:
        #4 turns
            #1 up
            #2 left/right
            #3 down
            #4 right/left
        #checks if it is already in a loop
        """TODO"""

        if move_history[0] == 'down':
            #3 done?
            pass
            if move_history[1] == 'left':
                #3, #2 done
                if move_history[2] == 'up':
                    #3, #2, #1 done
                    move = 'right'
                    inLoop_check = True
                else:
                    #3 and #2 done but in loop, thus #1 case
                    move = 'up'
            elif move_history[1] == 'right':
                #3, #2 done
                if move_history[2] == 'up':
                    #3, #2, #1 done
                    move = 'left'
                    inLoop_check = True
                else:
                    #3 and #2 done but in loop, thus #1 case
                    move = 'up'
            else:
                #3 done but not in loop, thus in #1 case
                move = 'up'

        else:
            #2 done?
            if (move_history[0] == 'right') or(move_history[0] =='left'):
                #2 done
                if move_history[1] == 'up':
                    #1 and #2 done so on step #3
                    move = 'down'
                else:
                    #2 done but not in loop, thus step #1
                    move = 'up'
            else:
                #1 done?
                if move_history[0] == 'up':
                    #on step 2
                    if 'left' in safe_choices:
                        move = 'left'
                    else:
                        move = 'right'
                else:
                    move = 'up'


    elif you_length is 5:
        pass
    elif you_length is 6:
        pass;
    else:
        print("ERROR SHOULDN'T BE HERE (make_young_loop)")

    if move in safe_choices:
        if inLoop_check is True:
            inLoop = True
    else:
        if inLoop_check is True:
            inLoop = False
        move = safe_choices[0]

    #debug print out
    if debug is True:
        print("\nmake_young_loop DEBUG:")
        print("-------------------")
        print("make_young_loop returns:")
        print("move: %s" % (move) )
        print("inLoop: %s" % (inLoop))
        print("-------------------")

    return move, inLoop

def stay_in_loop():
    #this will be hard
    move = 'left'

    return move

def make_head_box(board_matrix, food_location, you_length, head_xy, tail_loop_ready, inLoop, foodTrapped):
    #if headbox is complete will return tail_loop_ready = true and no move

    food_x = food_location['x']
    food_y = food_location['y']

    head_x = head_xy[0]
    head_y = head_xy[1]
    my_body = ['mh','mb','mt']
    choice = None

    #check if I can even head loop
    #if food on edge have to just go and eat food

    #if not on edge do a headbox

    if(you_length is 7):
        choice = None
        #will just do head loop #when done headloop will return inLoop to true
        pass
    else:
        #will see where it has completed a headbox
        if board_matrix[food_y - 1][food_x] in my_body:
            if board_matrix[food_y + 1][food_x] in my_body:
                if board_matrix[food_y][food_x - 1] in my_body:
                    if board_matrix[food_y][food_x + 1] in my_body:
                        if board_matrix[food_y+1][food_x+1] in my_body:
                            if board_matrix[food_y+1][food_x -1] in my_body:
                                if board_matrix[food_y-1][food_x+1] in my_body:
                                    if board_matrix[food_y-1][food_x-1] in my_body:
                                        tail_loop_ready = True
                                        choice = None
        else:
            if board_matrix[food_y - 1][food_x] is 'mh':
                #above
                choice = 'right'
            elif board_matrix[food_y -1][food_x+1] is 'mh':
                #top right
                choice = 'down'
            elif board_matrix[food_y][food_x+1] is 'mh':
                #right
                choice = 'down'
            elif board_matrix[food_y +1][food_x+1] is 'mh':
                #bottom right
                choice = 'left'
            elif board_matrix[food_y + 1][food_x] is 'mh':
                #bottom
                choice = 'left'
            elif board_matrix[food_y +1][food_x-1] is 'mh':
                #bottom left
                choice = 'up'
            elif board_matrix[food_y][food_x-1] is 'mh':
                #left
                choice = 'up'
            elif board_matrix[food_y-1][food_x-1] is 'mh':
                #top left_edge
                choice = 'right'

    if debug is True:
        print("\nmake_head_box DEBUG:")
        print("-------------------")
        print("make_head_box returns:")
        print("choice: %s" % (choice) )
        print("tail_loop_ready: %s" % (tail_loop_ready))
        print("inLoop: %s" % (inLoop))
        print("foodTrapped: %s" % (foodTrapped))
        print("-------------------")

    return choice, tail_loop_ready, inLoop, foodTrapped
