from Proj1.Astar import state, a_star
import sys
import argparse

default_puzzles = [('trivial', [[1, 2, 3], [4, 5, 6], [7, 8, 0]]),
                   ('very easy', [[1, 2, 3], [4, 5, 6], [7, 0, 8]]),
                   ('easy', [[1, 2, 0], [4, 5, 3], [7, 8, 6]]),
                   ('doable', [[0, 1, 2], [4, 5, 3], [7, 8, 6]]),
                   ('oh_boy', [[8, 7, 1], [6, 0, 2], [5, 4, 3]]),
                   ('impossible', [[2, 1, 3], [4, 5, 6], [7, 8, 0]])]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='', type=str, required=False)
    file = parser.parse_args().file
    if file != '':
        sys.stdin = open(file, 'r')

    size = input('Welcome to my puzzle solver, please enter the puzzle size: \n'
                 '\t3: 8-puzzle\n'
                 '\t4: 15-puzzle\n'
                 '\t5: 24-puzzle.\n')
    size = int(size)
    mode = 2
    if size == 3:
        mode = input('Type "1" to use a default puzzle, or "2" to create your own.\n')
        mode = int(mode)
    init_puzzle = [[] for j in range(size)]
    if mode == 2:
        print('Enter your puzzle, using a zero to represent the blank.\n'
              'Please only enter valid 8-puzzles.\n'
              'Enter the puzzle delimiting the numbers with a space.\n'
              'Type "ENTER" only when finished.')
        for i in range(size):
            s = input('Enter row {}: '.format(i))
            init_puzzle[i] = s.split()
            while len(init_puzzle[i]) != size:
                print('You should input {} integers. Please try again\n'.format(size))
                s = input('Enter row {}: '.format(i))
                init_puzzle[i] = s.split()
            for j in range(size):
                init_puzzle[i][j] = int(init_puzzle[i][j])
    else:
        dif = input('Please enter a desired difficulty on a scale from 0 to 5.\n')
        dif = int(dif)
        print('Difficulty of {} selected.'.format(default_puzzles[dif][0]))
        init_puzzle = default_puzzles[dif][1]
        print(init_puzzle)

    algo = input('Please select algorithm: \n'
                 '\t1: Uniform Cost Search\n'
                 '\t2: Misplaced Tile Heuristic\n'
                 '\t3: Manhattan Distance Heuristic.\n')
    algo = int(algo)

    interval = input('Please choose the evaluation interval, i.e., check the current state after how many steps:\n')
    interval = int(interval)

    _, _, _, t = a_star(init_puzzle, algo, interval)
