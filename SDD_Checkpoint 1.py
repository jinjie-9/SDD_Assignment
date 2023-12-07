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