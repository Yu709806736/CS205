import copy
import time
from typing import List, Tuple, Dict
from queue import PriorityQueue
import sys


class state:

    def __init__(self, puzzle: List[List[int]], g: int = 0, dis_method: int = 1, parent=None):
        """
        :param puzzle: the current puzzle state
        :param g: g(x)
        :param dis_method:  1 - Uniform Cost
                            2 - # Misplaced Tiles
                            3 - Manhattan Distance
        :param parent: the parent state of the current state
        """
        self.parent = parent
        self.puzzle = puzzle  # current puzzle
        self.g = g  # g(x)
        self.size = len(puzzle)  # puzzle size
        self.position: Dict[int, Tuple] = {}  # all positions - get coordinates by number in O(1)
        self.dis_method = dis_method  # algorithm
        self.is_goal = True  # whether it is goal state

        for i in range(self.size):
            for j in range(self.size):
                self.position[puzzle[i][j]] = (i, j)
                if puzzle[i][j] != 0 and puzzle[i][j] != (i * self.size + (j + 1)):
                    self.is_goal = False

        # get h(x)
        if dis_method == 1:
            self.h = 0
        elif dis_method == 2:
            self.h = self.mis_tile()
        elif dis_method == 3:
            self.h = self.dis_manh()
        else:
            print('Search algorithm should be: 1 for Uniform Cost Search, 2 for Misplaced Tile Heuristic, '
                  'or 3 for Manhattan Distance Heuristic.')

        self.fx = self.g + self.h

    def dis_manh(self) -> int:
        """
        :return: the Manhattan Distance to the goal state
        """
        res: int = 0
        for key in self.position.keys():
            if key != 0:
                i, j = self.position[key]
                res += abs((key - 1) // self.size - i) + abs((key - 1) % self.size - j)
        return res

    def mis_tile(self) -> int:
        """
        :return: the number of misplaced tiles
        """
        res: int = 0
        for key in self.position.keys():
            if key != 0:
                i, j = self.position[key]
                res += min(abs((key - 1) // self.size - i) + abs((key - 1) % self.size - j), 1)
        return res

    def check(self) -> bool:
        """
        :return:    True if reached the goal state
                    False if not reach the goal state
        """
        goal = [[j * self.size + (i + 1) for i in range(self.size)] for j in range(self.size)]
        goal[-1][-1] = 0
        for i in range(self.size):
            for j in range(self.size):
                if goal[i][j] != self.puzzle[i][j]:
                    return False
        return True

    def to_tuple(self) -> Tuple[Tuple[int]]:
        res = tuple(tuple(j for j in i) for i in self.puzzle)
        return res

    def generate_children(self, visited: Dict) -> List:
        """
        :param visited: all visited states
        :return:    If one of the children is goal state, only return goal state
                    all possible unvisited children if no one is goal state
        """
        r, c = self.position[0]
        res = []
        directions = [[0, 1], [1, 0], [-1, 0], [0, -1]]
        for dx, dy in directions:
            x = r + dx
            y = c + dy
            if 0 <= x < self.size and 0 <= y < self.size:
                puz = copy.deepcopy(self.puzzle)
                puz[r][c]: int = puz[x][y]
                puz[x][y] = 0
                st = state(puz, self.g + 1, self.dis_method, self)
                tup = st.to_tuple()
                if st.is_goal:
                    return [st]
                vis = visited.get(tup, [0, 0])
                if vis[0] == 0 or (vis[0] == 1 and st.g <= vis[1]):
                    res.append(st)
                    visited[tup] = [1, st.g]

        return res

    """
        the following four methods will help Priority queue to determine the object with higher priority
    """
    def __lt__(self, other):
        return self.fx < other.fx

    def __gt__(self, other):
        return self.fx > other.fx

    def __ge__(self, other):
        return self.fx >= other.fx

    def __le__(self, other):
        return self.fx <= other.fx

    def __eq__(self, other):
        return other.puzzle == self.puzzle

    def __str__(self):
        s = "The best state to expand with a g(n) = {0} and h(n) = {1} is...\n".format(self.g, self.h)
        for row in self.puzzle:
            s += '['
            for i in row:
                s += str(i)
                s += ', '
            s = s[:-2] + ']\n'
        return s


def a_star(init_puzzle: List[List[int]], algo=1, interval=1, time_limit=10, prt_path=True, prt_time=True) -> Tuple:
    """
    :param init_puzzle: initial puzzle
    :param algo: see class state @param dis_method
    :param interval: evaluation interval
    :param time_limit: time limit of the algorithm
    :param prt_path: whether print the solution's path
    :param prt_time: whether print the algorithm's running time
    :return: Tuple containing depth, number of node expanded, maximum size of the queue, and the
    """
    start = time.time()
    init_state = state(init_puzzle, 0, algo)  # create initial state object
    if init_state.is_goal:
        print('Step {0}: {1}'.format(0, init_state))
        print('Goal state!\n')
        print('Solution depth was {}'.format(0))
        print('Number of nodes expanded: {}'.format(0))
        print('Max queue size: {}'.format(0))
        return 0, 0, 0, 0
    # create visited dictionary: value[0]: 1 for added into queue, 2 for popped from queue, value[1]: g(x)
    visited = {init_state.to_tuple(): [1, 0]}
    pq = PriorityQueue()  # create priority queue
    pq.put([init_state.fx, init_state])  # add the initial state into the priority queue
    step = 0  # record the number of steps
    node = 1  # record the number of nodes expanded
    queue_max = 1  # record the maximum queue length
    while not pq.empty() and time.time() - start <= time_limit:
        f, st = pq.get()  # get the current best state in queue
        tup = st.to_tuple()
        if visited.get(tup)[0] <= 1:
            visited[tup][0] = 2
        else:
            continue
        if step % interval == 0:  # evaluation interval check
            print('Step {0}: {1}'.format(step, st))
        children: List[state] = st.generate_children(visited)  # get all possible children expanded from this state
        if not children or len(children) == 0:
            continue
        if children[0].is_goal:  # one of the children is the goal state
            depth = children[0].g
            final = children[0]
            print('Step {0}: {1}'.format(step + 1, children[0]))
            print('Goal state!\n')
            print('Solution depth was {}'.format(children[0].g))
            print('Number of nodes expanded: {}'.format(step))
            print('Max queue size: {}'.format(queue_max))
            break
        for child in children:  # put all children into pq
            pq.put([child.fx, child])
        if pq.qsize() > queue_max:  # update maximum queue length
            queue_max = pq.qsize()
        step += 1
    else:  # did not break the loop
        if pq.empty():
            print('Failure: Impossible to find a solution in .\n'
                  'Number of nodes expanded: {0}\n'
                  'Max queue size: {1}'.format(node, queue_max), file=sys.stderr)
        else:
            print('{0}s Time Limit Exceeded.'.format(time_limit))
        return 0, -1, 0, time_limit
    t = round((time.time()-start), 3)
    if prt_path:
        print_path(final)
    if prt_time:
        print('Algorithm takes: {} seconds.'.format(t))
    return depth, step, queue_max, t


def print_path(final: state):
    stt = copy.deepcopy(final)
    stack = [stt]
    while stt.parent is not None:
        stt = copy.deepcopy(stt.parent)
        stack.append(stt)

    while len(stack) >= 1:
        print(stack.pop())
