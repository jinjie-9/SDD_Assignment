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