import random

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
            print()
            print('5. Save game')
            print('0. Exit to main menu')
            choice = input('Input a Number as your choice (Example: 1)?: ')
            print('')

            if choice == '1' or choice == '2':
                if turn <= max_turns:  # Ensure turns don't exceed the maximum
                    if choice == '1':
                        buildbuildings(randno1, turn)
                    else:
                        buildbuildings(randno2, turn)
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
                return
            else:
                print("Invalid option. Try again.")

        turn += 1

    print('Final layout of Simp City:')
    map1(turn)
    score()

def savegame(turn, BuildingList):  # saves current game (Dani)
    file = open('save.txt', 'w')
    file.write('{}\n'.format(turn))  # writes the Turn
    for row in grid:
        line = ','.join(row)
        file.write(line + '\n')  # writes each row of the grid to the file
    building_list_str = ','.join(str(building) for building in BuildingList)
    file.write('{}\n'.format(building_list_str))  # adds remaining buildings to the text file
    file.close()
    print('Game Saved!')

def loadsgame(grid):  # loads the saved game (Dani)
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
        elif len(location) > 2 or not location[1:].isdigit():
            print('Input is invalid.')
        else:
            letter_location = location[0]
            num_location = int(location[1]) - 1

            if letter_location in letters and 0 <= num_location < 20:  # Validate the range
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

                    # Check if there's any non-empty space in the adjacent buildings
                    if any(building != '   ' for building in adjacent_buildings):
                        if grid[row][col] == '   ':
                            grid[row][col] = ' ' + BuildingName[randno] + ' '
                            break
                    else:
                        print('You must build next to an existing building.')
            else:
                print('Input is out of grid bounds.')



def buildingsremain():  # display the remaining buildings (Hadith)
    print('Building           Remaining')
    print('--------           ---------')
    for i in range(len(BuildingList)):
        print('{}                {}'.format(BuildingName[i], BuildingList[i]))


def score():
    residential_score = 0
    industry_score = 0
    commercial_score = 0
    park_score = 0
    road_score = 0
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
                industry_score += total_industries

            elif building == ' C ':
                adjacent_commercial = adj_buildings.count(' C ')
                commercial_score += adjacent_commercial

            elif building == ' O ':
                adjacent_parks = adj_buildings.count(' O ')
                park_score += adjacent_parks

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
    print(f"Residential Score: {residential_score}")
    print(f"Industry Score: {industry_score}")
    print(f"Commercial Score: {commercial_score}")
    print(f"Park Score: {park_score}")
    print(f"Road Score: {road_score}")
    print(f"Total Score: {total_score}")


def randbuilding(): # (Hadith)
    while True:
        randno = random.randint(0, 4)

        if BuildingList[randno] > 0:
            # Update BuildingList counts based on the generated building type
            BuildingList[randno] -= 1
            break

    return randno


while True: #(Travelle)
    global grid 
    grid = [['   ' for _ in range(20)] for _ in range(20)]  # 20x20 grid initialization
    
    BuildingName = ['R', 'I', 'C', 'O', '*']  # Residential, Industry, Commercial, Park, Road
    BuildingList = [8, 8, 8, 8, 8]  # Initial counts for each building type
    turn = 1

    print('Welcome, mayor of Ngee Ann City!')
    print('-----------------------------')
    print('1. Start a new game')
    print('2. Load saved game')
    print('0. Exit')
        
    choice = int(input('Input a Number as your choice (Example: 1): '))
    if choice == 0:
        print('Thanks for playing!')
        break
    elif choice == 1:
        gamestart(turn)
    elif choice == 2:
        turn, BuildingList = loadsgame(grid)
        gamestart(turn)
    else:
        print('That is an invalid option.')

