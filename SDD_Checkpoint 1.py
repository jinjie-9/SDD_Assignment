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

while True: #(Travelle)
    global grid 
    grid = [['   ' for _ in range(20)] for _ in range(20)]  # 20x20 grid initialization
    
    BuildingName = ['R', 'I', 'C', 'O', '*']  # Residential, Industry, Commercial, Park, Road
    BuildingList = [8, 8, 8, 8, 8]  # Initial counts for each building type
    turn = 1

    print('Welcome, mayor of Simp City!')
    print('-----------------------------')
    print('1. Start a new game')
    print('2. Load saved game')
    print('0. Exit')
    choice = int(input('Your choice?: '))
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

def gamestart(turn):  # main game (Hadith)
    max_turns = 400  # Adjust the maximum number of turns as needed

    while turn <= max_turns:
        randno1 = randbuilding()
        randno2 = randbuilding()

        while True:
            print('Turn {}'.format(turn))
            map1(turn)
            print('1. Build a {}'.format(BuildingName[randno1]))
            print('2. Build a {}'.format(BuildingName[randno2]))
            print('3. See remaining buildings')
            print('4. See current score')
            print()
            print('5. Save game')
            print('0. Exit to main menu')
            choice = input('Your choice?: ')

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