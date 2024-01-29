
import random

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }

archer = {'shortform' : 'ARCHR',
          'name': 'Archer',
          'maxHP': 5,
          'min_damage': 1,
          'max_damage': 4,          
          'price': 5,
          'upgrade_cost': 8
          }
             
wall = {'shortform': 'WALL',
        'name': 'Wall',
        'maxHP': 20,
        'min_damage': 0,
        'max_damage': 0,
        'price': 3,
        'upgrade_cost': 6
        }

zombie = {'shortform': 'ZOMBI',
          'name': 'Zombie',
          'maxHP': 15,
          'min_damage': 3,
          'max_damage': 6,
          'moves' : 1,
          'reward': 2
          }

werewolf = {'shortform': 'WWOLF',
            'name': 'Werewolf',
            'maxHP': 10,
            'min_damage': 1,
            'max_damage': 4,
            'moves' : 2,
            'reward': 3
            }

cannon = {'shortform': 'CANON',
            'name': 'Cannon',
            'maxHP': 10,
            'min_damage': 3,
                  
            'max_damage': 5,
            'price' : 7,
            'cannon_ready' : True
            }

skeleton = {'shortform': 'SKELE',
            'name': 'Skeleton',
            'maxHP': 10,
            'min_damage': 1,
            'max_damage': 3,
            'moves' : 1,
            'reward': 3
            }
            

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]

monster_list = [zombie, werewolf, skeleton]

defender_list = [archer, wall, cannon]

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


#----------------------------------------------------------------------
# draw_field()                 
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field():
    num_column = len(field[0])
    num_row = len(field)
    print("  {:^5} {:^5} {:^5}".format("1","2","3"))
    for row in range(num_row):
        print(" +", end = "")
        for border in range(num_column):
            print("-----", end = "+")    
        print()
        
        print(alphabet[row], end = "|")
        for i in field[row]:
            if i == None:
                print("{:^5}".format("")
                  , end = "|")
            else:                                                    # Condition for if there is a monster/ defender at that square                    
                print("{:^5}".format(i[0]["shortform"]), end = "|")  # i[0] is the dictionary of unit
        print()
        print(" |", end = "")
        for i in field[row]:
            if i == None:
                print("{:^5}".format(""), end = "|")
            else:                                                           # Condition for if there is a monster/ defender at that square 
                print("{:>2}/{:<2}".format(i[1],i[0]["maxHP"]), end = "|")  # i[1] is the health of the monster/ defender
            
        print()
    print(" +", end = "")
    for column in range(len(field[0])):
        print("-----", end = "+")    
    print()
    
    return

#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):
    print("1. Buy unit        2. End turn")
    print("3. upgrade unit    4. save game")
    print("5. Quit")
    
#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Game options")
    print("4. Quit")

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name):         # unit_name is the dictionary of the unit
    column = position[1]
    row = position[0]
    
    if row >= len(field):
        return False
    
    if column >= len(field[0]):
        return False
    
    if unit_name in defender_list:
        if column >= 3:
            return False
        
    if field[row][column] != None:
        return False

    health = unit_name["maxHP"]
    
    if unit_name == cannon:         
        field[row][column] = [unit_name, health, unit_name['cannon_ready']]         # For defender cannon only    
    else:
        field[row][column] = [unit_name, health]                                                        
    return True 

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, game_vars):
    print("What unit do you wish to buy?")
    print("1. Archer(5 gold)")
    print("2. Wall (3 gold)")
    print("3. Cannon (7 gold)")
    print("4. Don't buy")
    choice = input("Your choice? ")
    if choice != '1' and choice != '2' and choice != '3' and choice != '4' :        # Validation
        print("Invalid input. Try again!")
        buy_unit(field, game_vars)

    elif choice == '1' or choice == '2' or  choice == '3':
        if choice == '1':
            unit_name = archer                                              
            if game_vars['gold'] < unit_name['price']:
                print("Purchase Failed! Insufficient gold. ")
                buy_unit(field, game_vars)
                return
        elif choice == '3':
            unit_name = cannon
            if game_vars['gold'] < unit_name['price']:
                print("Purchase Failed! Insufficient gold. ")
                buy_unit(field, game_vars)
                return
        else:
            unit_name = wall
            if game_vars['gold'] < unit_name['price']:
                print("Purchase Failed! Insufficient gold. ")
                buy_unit(field, game_vars)
                return
        
        position = input("Place Where?")
        if position[0].isalpha() and position[1].isdigit() and len(position) == 2:          # Validation
            position = position.upper()
            position = [alphabet.index(position[0]),int(position[1]) - 1 ]
            valid = place_unit(field, position, unit_name)
            
            if valid == True:
                game_vars['gold'] -= unit_name['price']
                return
            elif valid == False:
                print("Invalid position. Try again!")
                buy_unit(field, game_vars)
        else:
            print("Invalid position. Try again!")
            buy_unit(field, game_vars)
                
    return

#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(defender_name, field, row, column):                                         # defender_name is the list of the defender in the field [defender(dict), hp]
    damage = random.randint(defender_name[0]['min_damage'],defender_name[0]['max_damage'])          
    for i in range(column,len(field[row])):
        lane = field[row]
        if lane[i] != None and lane[i][0] in monster_list:                                      # If statement to check if column of the lane (lane[i]) has a monster in it
            monster = lane[i]                                                               # monster is the list of the monster in the field [monster(dict), hp]
            
            if defender_name[0] == archer:
                if monster[0] == skeleton:
                    damage = damage//2
                                    
                print("{} in lane {} shoots {} for {} damage!"
                        .format(defender_name[0]['name'], alphabet[row],monster[0]['name'],damage))
                monster[1] -= damage

                # If monster dies
                if monster[1] <= 0:                                                         
                    lane[i] = None
                    game_vars["monsters_killed"] += 1
                    print("{} dies!".format(monster[0]["name"]))
                    game_vars["gold"] += monster[0]["reward"]
                    game_vars['num_monsters'] -= 1
                    game_vars['threat'] += monster[0]["reward"]
                    print("You gain {} gold as a reward.".format(monster[0]["reward"]))
                   
                       
            if defender_name[0] == cannon:
                # If cannon is ready
                if defender_name[2] == True:
                    defender_name[2] = False
                    print("{} in lane {} shoots {} for {} damage!"
                        .format(defender_name[0]['name'], alphabet[row],monster[0]['name'],damage))
                    monster[1] -= damage

                    # If monster dies
                    if monster[1] <= 0:
                        lane[i] = None
                        game_vars["monsters_killed"] += 1
                        print("{} dies!".format(monster[0]["name"]))
                        game_vars["gold"] += monster[0]["reward"]
                        game_vars['num_monsters'] -= 1
                        game_vars['threat'] += monster[0]["reward"]
                        print("You gain {} gold as a reward.".format(monster[0]["reward"]))
                        
                    else:
                        knock_back = random.randint(1,2)                         # 50% chance of knocking back monster
                        if i != len(field[row]) - 1:                             # Condition for if Monster is not at the end of the lane
                            if knock_back == 1:                                                     
                                x = lane[i]
                                lane[i + 1] = x
                                lane[i] = None
                                print("{} in lane {} knocked back!".format(monster[0]['name'],alphabet[row]))   
                                
                # If cannon is not ready    
                elif defender_name[2] == False:
                    defender_name[2] = True
                    
            break
            

    return
#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(monster_name, field, row, column):
    lane = field[row]

    for i in range(monster_name[0]['moves']):
        if column == 0:
            return True
        
        if lane[column-1] != None:                                                                          # Condition for if column infront of the monster is occupied
            if lane[column-1][0] in defender_list:                                                              # Condition for if column infront of the monster is a defender
                damage = random.randint(monster_name[0]['min_damage'],monster_name[0]['max_damage'])
                defender = lane[column-1]                                                                       # defender is this list of the defender in the field [defender(dict), hp]
                defender[1] -= damage                                                                           
                print("{} in lane {} hit {} for {} damage!"
                            .format(monster_name[0]['name'], alphabet[row],defender[0]['name'],damage))
                        
                # If defender dies
                if defender[1] <= 0:                                                                            
                    print("{} dies!".format(defender[0]["name"]))
                    lane[column-1] = None
                    column -= 1
                    
            else:
                print("{} in lane {} is blocked from advancing.".format(monster_name[0]['name'],alphabet[row]))
        else:
            x = lane[column]
            lane[column - 1] = x
            lane[column] = None
            print("{} in lane {} advances!".format(monster_name[0]['name'],alphabet[row]))
            column -= 1
                
         
    
    return False

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, monster_list):
    game_vars['num_monsters'] += 1
    # Random lane
    row = random.randint(0,len(field)-1)
    
    column = len(field[0])-1
    # Random monster
    unit_name = random.choice(monster_list)
    
    position = [row,column]
    valid = place_unit(field, position, unit_name)
    
    if valid == True:
        return
    
    if valid == False:
        spawn_monster(field, monster_list)
        
        

    return

#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game():
    path = "D:\\documents\\programing 1\\Assignment\\"
    file = open(path + "save.txt" , "w")
    # saving game_vars
    for key in game_vars:        
        file.write("{},".format(game_vars[key]))
    file.write("\n")

    # saving all defender        
    for defender in defender_list:
        for key in defender:
            file.write("{},".format(defender[key]))
        file.write("\n")

    # saving all monster
    for monster in monster_list:
        for key in monster:
            file.write("{},".format(monster[key]))
        file.write("\n")

    # saving field
    for row in field:
        for column in row:
            if column != None:
                if column[0]['name'] != 'Cannon':
                    file.write("{}/{},".format(column[0]['name'],column[1]))
                else:
                    file.write("{}/{}/{},".format(column[0]['name'],column[1],column[2]))
            else:
                file.write("{},".format(column))
        file.write("\n")
        
        
            
            
    file.close()
    print("Game saved!")

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game(game_vars):
    path = "D:\\documents\\programing 1\\Assignment\\"
    file = open(path + "save.txt" , "r")
    data = []
    
    for x in file:
        x = x.strip("\n").split(',')
        x.remove("")
        data.append(x)
    file.close()
    
    row = 0
    column = 0
    # loading game_vars
    for key in game_vars:
        if data[row][column].isdigit() == True:
                game_vars[key] = int(data[row][column])
        else:
            stats[key] = data[row][column]
        column += 1
    row += 1

    # loading all defender
    for defender in defender_list:        
        column = 0
        for key in defender:
            
            if data[row][column].isdigit() == True:
                defender[key] = int(data[row][column])
            elif data[row][column] == 'True':
                defender[key] = True
            elif data[row][column] == 'False':
                defender[key] = False
            else:
                defender[key] = data[row][column]
            column += 1
        row += 1
        
    # loading all monster    
    for monster in monster_list:        
        column = 0
        for key in monster:            
            if data[row][column].isdigit() == True:
                monster[key] = int(data[row][column])
            else:
                monster[key] = data[row][column]
            column += 1
        row += 1        
    field = []
    
    # For what is left in the file that is not loaded (field)
    # loading field
    for lane in range(len(data)-row):
        column = 0
        x = []
        for position in range(len(data[row])):
            if data[row][column] != 'None':
                data[row][column] = data[row][column].split("/")
                
                for i in monster_list:
                    if data[row][position][0] == i['name']:
                        unit = [i,int(data[row][column][1])]
                        x.append(unit)
                        
                for i in defender_list:
                    if data[row][position][0] == i['name']:
                        if i['name'] != "Cannon":
                            unit = [i,int(data[row][column][1])]
                            x.append(unit)
                        else:
                            if data[row][column][2] == 'True':
                                data[row][column][2] = True
                            elif data[row][column][2] == 'False':
                                data[row][column][2] =False
                            unit = [i,int(data[row][column][1]),data[row][column][2]]
                            x.append(unit)
            else:
                x.append(None)
            column += 1
            
        field.append(x)
        row += 1                        
    return field


#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 0
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars['threat'] = 0
    game_vars['max_threat'] = 10
    game_vars['danger_level'] = 1

#----------------------------------------------------
# upgrade_unit(archer,wall,game_vars)
#
#   Give option to upgrade units
#----------------------------------------------------
def upgrade_unit(archer,wall,game_vars):
    print("What unit do you wish to Upgrade?")
    print("1. Archer({} gold)".format(archer['upgrade_cost']))
    print("2. Wall ({} gold)".format(wall['upgrade_cost']))
    print("3. Don't upgrade")
    
    
    option  = input("Your choice? ")
    
    if option != '1' and option != '2' and option != '3' :      # Validation
        print("Invalid input. Try again!")
        upgrade_unit(archer,wall,game_vars)
        
    elif option == '1':
        if game_vars['gold'] < archer['upgrade_cost']:
            print("Purchase Failed! Insufficient gold. ")
            upgrade_unit(archer,wall,game_vars)
        archer['maxHP'] += 1
        archer['min_damage'] += 1
        archer['max_damage'] += 1
        game_vars['gold'] -= archer['upgrade_cost']
        print("Upgrade successful!")
        archer['upgrade_cost'] += 2
        start_game(game_vars)
        
    elif option == '2':
        if game_vars['gold'] < wall['upgrade_cost']:
            print("Purchase Failed! Insufficient gold. ")
            upgrade_unit(archer,wall,game_vars)
        wall['maxHP'] += 5
        
        game_vars['gold'] -= wall['upgrade_cost']
        print("Upgrade successful!")
        wall['upgrade_cost'] += 2
        start_game(game_vars)
        
    elif option == '3':
        start_game(game_vars)

    return

#----------------------------------------------------
# game_options(field,game_vars)
#
#   Allow players to specify various game options,
#----------------------------------------------------
def game_options(field,game_vars):
    game_vars['turn'] = 0
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars['threat'] = 0
    game_vars['danger_level'] = 1
    
    target =  int(input("Enter number of kills needed to win: "))
    game_vars['monster_kill_target'] = target

    threat = int(input("Enter threat meter length: "))
    game_vars['max_threat'] = threat

    lane = int(input("Enter number of lanes (max: 26): "))
    if lane > 26 or lane < 1:
        print("Input out of range. Try again!")
        game_options(field,game_vars)    
    length = int(input("Enter length of each lane (min: 4): "))
    if length < 4:
        print("Input out of range. Try again!")
        game_options(field,game_vars) 
        
    field = []
    for row in range(lane):
        L = []
        for column in range(length):
            L.append(None)
        field.append(L)
    
    return field
        

        
#-------------------------------------------
#  start_game(game_vars)
#
# allows the game to start
#------------------------------------------
def start_game(game_vars):
    if game_vars['num_monsters'] == 0:    
        spawn_monster(field, monster_list)
    if game_vars['threat'] >= game_vars['max_threat']:
        while game_vars['threat'] >= game_vars['max_threat']:
            spawn_monster(field, monster_list)
            game_vars['threat'] -= game_vars['max_threat']

    if game_vars['turn'] % 12 == 0:
        game_vars['danger_level'] += 1
        for i in monster_list:
            i['maxHP'] += 1
            i['min_damage'] += 1
            i['max_damage'] += 1
            i['reward'] += 1
        print("The evil grows stronger!")
        
    draw_field()
    
    print("Turn {:<2}     Threat = [".format(game_vars['turn']), end = '')
    for i in range(game_vars['threat']):
        print("-", end = '')
    for i in range(game_vars['max_threat'] - game_vars['threat']):
        print(" ", end = '')
    print("]     Danger Level {}".format(game_vars['danger_level']))
    print("Gold = {:<2}     Monsters killed = {}/{}"\
          .format(game_vars['gold'],game_vars['monsters_killed'],game_vars['monster_kill_target']))


    show_combat_menu(game_vars)
    option = input("Your choice?")
    if option != '1' and option != '2' and option != '3' and option != '4' and option != '5':
        print("Invalid input. Try again!")
        start_game(game_vars)
        
    elif option == '1' or option == '2':
        if option == '1':
            buy_unit(field, game_vars)
        game_vars['turn']+=1
            
        for row in range(len(field)):
            lane = field[row]
            # find defenders in the lane
            for column in range(len(lane)):
                if lane[column] != None and lane[column][0] in defender_list:
                    defender_name = lane[column]
                    defender_attack(defender_name, field, row, column)
            if game_vars['monsters_killed'] == game_vars['monster_kill_target']:
                print("You have protected the city! You win!")
                return
                
            # find monster in the lane             
            for column in range(len(lane)):
                if lane[column] != None and lane[column][0] in monster_list:
                    monster_name = lane[column]
                    win_condition = monster_advance(monster_name, field, row, column)
                    if win_condition == True:
                        print("A {} has reached the city! All is lost".format(monster_name[0]['name']))
                        return
                                                
        game_vars['gold'] += 1
        game_vars["threat"] += random.randint(1,game_vars["danger_level"])
        
            
        start_game(game_vars)
        
    elif option == '3':
        
        upgrade_unit(archer,wall,game_vars)
        
    elif option == '4':
        save_game()
        start_game(game_vars)
    
    elif option == '5':
        print("See you next time!")
        return

    return




#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()

# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
while True:
    show_main_menu()
    choice = input("Your choice?")
    if choice == '1':
        initialize_game()
        game_vars['turn']+=1
        start_game(game_vars)
        break
         
    elif choice == '2':
        field = load_game(game_vars)
        start_game(game_vars)
        break

            
    elif choice == '3':
        field = game_options(field,game_vars)
        game_vars['turn']+=1
        start_game(game_vars)
        break

    elif choice == '4':
        print("See you next time!")
        break
            
    else:
        print("Invalid input.")
        continue
