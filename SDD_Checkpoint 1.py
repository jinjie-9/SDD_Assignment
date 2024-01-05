import random
import os
import pickle as c


load = True
game_vars = {}
def init(): #initialising the game and the variables
    global game_vars
    game_vars = { # default values
    "Coin": 16,
    "Total_score": 0
    }
    if os.stat("save.txt").st_size == 0: # To check if there is a save in the file
        global load
        load = False                          # If there is no save, load is set to false
    else:
        load = True  

def map1(turn): # prints grid (Jin Jie and Travelle)
    print('       A       B       C       D       E       F       G       H       I       J       K       L       M       N       O       P       Q       R       S       T')
    num_of_row = len(grid)
    num_of_column = len(grid[0])
    print('    ', end='')
    for cols in range(num_of_column):
        print('+-------', end='')
    print('+')
    i = 1
    for row in range(num_of_row):
        if i < 10:
            print('0{}'.format(i), end='')
        else:
            print('{}'.format(i), end='')
        i += 1
        for cols in grid[row]:
            print('  | {} '.format(cols), end='')
        print('  |')
        print('    ', end='')
        for cols in range(num_of_column):
            print('+-------', end='')
        print('+')

def gamestart(turn):  # main game (Hadith)
    max_turns = 400  # Adjust the maximum number of turns as needed

    while turn <= max_turns:
        randno1 = randbuilding()
        randno2 = randbuilding()

        while randno1 == randno2:
            randno2 = randbuilding()

        while True:
            print('Turn {}'.format(turn))
            map1(turn)
            
            
            print('R is Residential')
            print('I is Industry')
            print('C is Commercial')
            print('O is Park')
            print('* is Road')
            print('')
            print('1. Build a {}'.format(BuildingName[randno1]))
            print('2. Build a {}'.format(BuildingName[randno2]))
            

            print('3. See remaining buildings')
            print('4. See current score')
            print('5. Save game')
            print('0. Exit to main menu')
            print()
            print(f'Coins: {game_vars["Coin"]}')
            print()
            print()
            choice = input('Input a Number as your choice (Example: 1)?: ')
            print('')

            if choice == '1' or choice == '2':
                if turn <= max_turns:  # Ensure turns don't exceed the maximum
                    if choice == '1':
                        board_is_full = buildbuildings(randno1, turn)
                    else:
                        board_is_full = buildbuildings(randno2, turn)
                    if board_is_full == True:
                        print("Game completed!")
                        return 0
                    if game_vars['Coin'] == 0:
                        print("Game over!")
                        return 0
                    break
                else:
                    print("You've reached the maximum turns.")
            elif choice == '3':  # see remaining buildings
                buildingsremain()
            elif choice == '4':  # see current score
                score()
            elif choice == '5':  # save game
                savegame(turn, BuildingList)
            elif choice == '0':  # exit game
                checkfiles()  
                return
            else:
                print("Invalid option. Try again.")

        turn += 1

    print('Final layout of Ngee Ann City:')
    map1(turn)
    score()


###################### files and saves #############################

def checkfiles():
    print("Checking files")
    files_to_check = ["save.txt", "scores.txt"]
    file_names = os.listdir()
    index = 1
    for file in files_to_check:
        if file in file_names:
            print(f"Checking {index}/{len(files_to_check)}")
        else:
            print(f"Adding missing files {index}/{len(files_to_check)}")
            f = open(file, '+a')
            f.close()
        index+=1
    if os.stat("scores.txt").st_size == 0:
        with open("scores.txt", 'a') as file:
            file.write("position, name, score\n")
    return

def savegame(turn, BuildingList):  # saves current game (Dani)
    file = open('save.txt', 'w')
    file.write('{}\n'.format(turn))  # writes the Turn
    for row in grid:
        line = ','.join(row)
        file.write(line + '\n')  # writes each row of the grid to the file
    building_list_str = ','.join(str(building) for building in BuildingList)
    file.close()
    print('Game Saved!')

def savescore(score):
    file = open('scores.txt', 'w')
    file.write("{}\m".format(score))

def loadsgame(grid):  # loads the saved game (Dani)
    if (load == False):
        return turn, BuildingList
    datafile = open("save.txt", "r")
    dataline = datafile.readlines()
    # get gameturn
    turn = int(dataline[0].strip())

    # get the grid
    for i in range(20):  # Adjust the range to cover the 20x20 grid
        temp_grid_list = []
        line = dataline[i + 1].replace('\n', '')
        temp_grid_list = line.split(',')
        grid[i] = temp_grid_list

    building_list_str = dataline[21].strip()  # Assuming BuildingList is in the last line
    BuildingList = [int(building) for building in building_list_str.split(',')]

    return turn, BuildingList


def buildbuildings(randno, turn): # (Javier and Dani)
    letters = [chr(97 + i) for i in range(20)]  # a-z
    numbers = [i for i in range(20)]  # 0-19

    while True:
        location = input('Build where? (e.g., a5): ')
        location = location.lower()  # lc
        if len(location) <= 1:
            print('That is an invalid option.')
        elif len(location) > 3 or not location[1:].isdigit():
            print('Input is invalid.')
        else:
            letter_location = location[0]
            num_location = int(location[1:]) - 1

            if letter_location in letters and 0 <= num_location <= 20:  # Validate the range
                col = letters.index(letter_location)
                row = num_location

                if turn == 1:
                    if grid[row][col] == '   ':
                        grid[row][col] = ' ' + BuildingName[randno] + ' '
                        break
                else:
                    adjacent_buildings = []
                    if row > 0:
                        adjacent_buildings.append(grid[row - 1][col])
                    if row < 19:
                        adjacent_buildings.append(grid[row + 1][col])
                    if col < 19:
                        adjacent_buildings.append(grid[row][col + 1])
                    if col > 0:
                        adjacent_buildings.append(grid[row][col - 1])

                    if any(building != '   ' for building in adjacent_buildings):
                        if grid[row][col] == '   ':
                            building_type = BuildingName[randno]
                            grid[row][col] = ' ' + building_type + ' '

                            # Update coins for placing an 'R' adjacent to 'I' and 'C'
                            if building_type == 'R':
                                coin_gain = adjacent_buildings.count(' I ') + adjacent_buildings.count(' C ')
                                game_vars['Coin'] += coin_gain
                            # Update coins for placing an 'I' or 'C' adjacent to 'R'
                            elif building_type in ['I', 'C']:
                                coin_gain = adjacent_buildings.count(' R ')
                                game_vars['Coin'] += coin_gain

                            break
                    else:
                        print('You must build next to an existing building.')
                
            else:
                print('Input is out of grid bounds.')
    game_vars['Coin'] -= 1
    score()
    return is_board_full(grid)

def buildingsremain():  # display the remaining buildings (Hadith)
    print('Building           Remaining')
    print('--------           ---------')
    for i in range(len(BuildingList)):
        print('{}                {}'.format(BuildingName[i], BuildingList[i]))

def is_board_full(grid):
    for row in grid:
        for cell in row:
            if cell == '   ':  # Assuming '   ' represents an empty cell
                return False  # Board is not full
    return True  # Board is full

def score():
    residential_score, industry_score, commercial_score, park_score, road_score = 0, 0, 0, 0, 0
    total_industries = sum(row.count(' I ') for row in grid)  # Count total industries

    for row in range(len(grid)):
        connected_roads = 0  # Reset for each row
        for col in range(len(grid[0])):
            building = grid[row][col]
            adj_buildings = []

            # Check adjacent buildings
            if col > 0:
                adj_buildings.append(grid[row][col - 1])  # Left
            if col < len(grid[0]) - 1:
                adj_buildings.append(grid[row][col + 1])  # Right
            if row > 0:
                adj_buildings.append(grid[row - 1][col])  # Up
            if row < len(grid) - 1:
                adj_buildings.append(grid[row + 1][col])  # Down

            if building == ' R ':
                if ' I ' in adj_buildings:
                    residential_score += 1
                else:
                    adjacent_R_or_C = adj_buildings.count(' R ') + adj_buildings.count(' C ')
                    adjacent_parks = adj_buildings.count(' O ')
                    residential_score += adjacent_R_or_C + 2 * adjacent_parks

            elif building == ' I ':
                industry_score += 1 
                # Coins generated by industries adjacent to residential buildings can be calculated here if needed

            elif building == ' O ':
                # Score for parks: 1 point if at least one adjacent building is a park
                if adj_buildings.count(' O ') > 0:
                    park_score += 0.5


            elif building == ' C ':
                # Score for parks: 1 point if at least one adjacent building is a park
                if adj_buildings.count(' C ') > 0:  
                    commercial_score += 0.5

            elif building == ' * ':
                # Count connected roads in the row
                if connected_roads == 0 or (col > 0 and grid[row][col - 1] == ' * '):
                    connected_roads += 1
                else:
                    road_score += connected_roads
                    connected_roads = 1

        # Add the score for the last set of connected roads in the row
        road_score += connected_roads

    total_score = residential_score + industry_score + commercial_score + park_score + road_score
    game_vars['Total_score'] = total_score
    # Here you can also calculate and store the total coins generated
    # print(f"Residential Score: {residential_score}")
    # print(f"Industry Score: {industry_score}")
    # print(f"Commercial Score: {commercial_score}")
    # print(f"Park Score: {park_score}")
    # print(f"Road Score: {road_score}")
    print(f"Total Score: {total_score:.0f}")
    print()
    



def displayScores():
    score = read_scores()
    print("position name score")
    for i in range(len(score)):
        print("")
        for j in range(len(score[i])):
            print(score[i][j], end=' ')
    print("")
    return

def randbuilding(): # (Hadith)
    while True:
        randno = random.randint(0, 4)

        if BuildingList[randno] > 0:
            # Update BuildingList counts based on the generated building type
            BuildingList[randno] -= 1
            break

    return randno
def read_scores():
    scores = []
    with open("scores.txt", 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            if line.strip():  # Ignore empty lines
                parts = line.split()
                if len(parts) >= 3:
                    position = parts[0].rstrip('.')
                    name = ' '.join(parts[1:-1])
                    score = parts[-1]
                    scores.append([position, name, score])
    return scores


def update_scores_file(file_path, updated_list):
    with open(file_path, 'w') as file:
        # Write the header
        file.write('position, name, score\n')

        # Write the updated list
        for item in updated_list:
            position, name, score = item
            file.write(f"{position}. {name} {score}\n")

init()
checkfiles()  
while True: #(Travelle)


    global grid 
    grid = [['   ' for _ in range(20)] for _ in range(20)]  # 20x20 grid initialization
    
    BuildingName = ['R', 'I', 'C', 'O', '*']  # Residential, Industry, Commercial, Park, Road
    BuildingList = [8, 8, 8, 8, 8]  # Initial counts for each building type
    turn = 1
    coins = 16
    print()
    print('Welcome, mayor of Ngee Ann City!')
    print('-----------------------------')
    print('1. Start a new game')
    if load == False:
        print('2. Load saved game (no save found)')
    else: print('2. Load saved game')
    print('3. Display Top 10 Scores')
    print('0. Exit')
    check_state = 1
    while True:
        try:
            choice = int(input('Input a Number as your choice (Example: 1): '))
            break
        except:
            print("Invalid Input")

    if choice == 0:
        print('Thanks for playing!')
        
        break
    elif choice == 1:
        check_state = gamestart(turn)
    elif choice == 2:
        try:
            turn, BuildingList = loadsgame(grid)
            
        except:
            print("No saves found")
        check_state = gamestart(turn)
    elif choice == 3:
        displayScores()
    else:
        print('That is an invalid option.')

    if check_state == 0: 
        scores = read_scores()
        if len(scores) < 10:
            username = input("type username(spaces will be removed): ")
            username.replace(" ", "")
            if len(scores) == 0:
                scores.append(["1", f"{username}", f"{game_vars['Total_score']}"])
                update_scores_file("scores.txt", scores)
            else:
                for i in range(len(scores)):
                    if game_vars['Total_score'] > int(scores[i][2]):
                        
                        prev_rec = []
                        for j in scores[i]:
                            prev_rec.append(j)
                        new_pos = int(prev_rec[0]) + 1
                        prev_rec[0] = new_pos
                        scores[i][2] = game_vars['Total_score']
                        scores[i][1] = username

                        scores.insert(new_pos + 1, prev_rec)
                        for i in range(len(scores)):
                            if i > new_pos - 1:
                                scores[i][0] = int(scores[i][0]) + 1 
                        break
                    else:
                        scores.append([10, username, game_vars['Total_score']])
                        break          
                update_scores_file("scores.txt", scores)
            
        elif len(scores) == 10:
            username = input("type username(spaces will be removed): ")
            username.replace(" ", "")
            for i in range(len(scores)):
                if game_vars['Total_score'] > int(scores[i][2]):
                    scores[i][2] = game_vars['Total_score']
                    scores[i][1] = username
                    break
            update_scores_file("scores.txt", scores)
        
        break

