# CS205 Project 1
8-puzzle solver
### Files
- [Astar.py](https://github.com/Yu709806736/CS205/blob/main/Proj1/Astar.py): the A* algorithm with no heuristic, misplaced tiles heuristic, or Manhattan distance heuristic.
- [plot.py](https://github.com/Yu709806736/CS205/blob/main/Proj1/plot.py): experiment result visualization
- [main.py](https://github.com/Yu709806736/CS205/blob/main/Proj1/main.py): a demo of how to use the A*
- [1.in](https://github.com/Yu709806736/CS205/blob/main/Proj1/1.in): a test case
- Images: experiment results
### Usage
    python main.py --file 1.in
    python plot.py
### Result - comparison of the three algorithms
A* terminated after 5 seconds  
- Total number of expanded nodes w.r.t. depths for each algorithm:  
![image1](https://github.com/Yu709806736/CS205/blob/main/Proj1/nodes_expanded_depth.jpg)
- Running time w.r.t. depths for each algorithm:  
![image2](https://github.com/Yu709806736/CS205/blob/main/Proj1/time_depth.jpg)
