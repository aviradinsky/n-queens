# -*- coding: utf-8 -*-
"""DFS_queens.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1puD0kHn_0jLIZbtEOzNW4Atp2JNHcaYB

This is the notebook version of the code. I will use this to explain the homework.  I used parts of the code from: https://www.sanfoundry.com/python-program-solve-n-queen-problem-without-recursion/

As we did in class, we will represent the board as a one-dimensional array where each position in the arrray is the n'th queen's column value. So if the array is: [1, 3, 0, 2], then the first queen in the first row is in position 1 (from 0--3), the queen in the second row is in position 3 (the last column), the queen in the third row is in the first column and the last queen is the in the second position.
"""

columns = [] #columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
size = 30
import random #hint -- you will need this for the following code: column=random.randrange(0,size)
from sys import stderr
import copy
"""Let's setup one iteration of the British Museum algorithm-- we'll put down 4 queens randomly."""

def place_n_queens(size):
    columns.clear()
    row = 0
    while row < size:
        column=random.randrange(0,size)
        columns.append(column)
        row+=1

# place_n_queens(size)

"""Now, we can print the result with a simple loop:"""

def display():
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()

def edisplay():
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ', file=stderr)
            else:
                print('.', end=' ', file=stderr)
        print(file=stderr)
# place_n_queens(size)
# display()
# print(columns)

"""This of course is not necessary legal, so we'll write a simple DFS search with backtracking:"""

def dfs(size):
    columns.clear()
    number_of_moves = 0 #where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0
    row = 0
    column = 0
    # iterate over rows of board
    while True:
        #place queen in next row
        #print(columns)
        #print("I have ", row, " number of queens put down")
        #display()
        # print(number_of_moves)
        while column < size:
            number_of_iterations+=1
            if next_row_is_safe(column):
                place_in_next_row(column)
                number_of_moves += 1
                row += 1
                column = 0
                break
            else:
                column += 1
        # if I could not find an open column or if board is full
        if (column == size or row == size):
            number_of_iterations+=1
            # if board is full, we have a solution
            if row == size:
                # print("I did it! Here is my solution")
                # display()
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            if (prev_column == -1): #I backtracked past column 1
                # print("There are no solutions")
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column

"""This code is nice, but it uses three functions:

1. place_in_next_row

2. remove_in_current_row

3. next_row_is_safe

That we now have to define


"""

def place_in_next_row(column):
    columns.append(column)

def remove_in_current_row():
    if len(columns) > 0:
        return columns.pop()
    return -1

def next_row_is_safe(column):
    row = len(columns)
    # check column
    for queen_column in columns:
        if column == queen_column:
            return False

    # check diagonal
    for queen_row, queen_column in enumerate(columns):
        if queen_column - queen_row == column - row:
            return False

    # check other diagonal
    for queen_row, queen_column in enumerate(columns):
        if ((size - queen_column) - queen_row
            == (size - column) - row):
            return False
    return True

def correct() -> bool:
    # take in [1,3,5] as the board
    if len(set(columns)) != size:
        return False

    for (i0, a) in enumerate(columns):
        for (i1, b) in enumerate(columns):
            if i0 == i1: continue
            if abs(i0 - i1) == abs(a - b) or a == b:
                return False
    return True

def british_museum(size: int) -> tuple[int, int]:
    # randomly place queens on the board and check if correct
    place_n_queens(size)
    count = 1
    while not correct():
        place_n_queens(size)
        count += 1
    return count, count * 8

def heuristic_stochastic(size: int) -> tuple[int, int]:
    number_of_moves = 0 #where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0
    # randomly place queens on the board
    place_n_queens(size); number_of_moves += 8
    while True:
        number_of_iterations += 1
        # get the heuristic score of the board
        scores = hscore()
        total_score = sum(scores)
        if total_score == 0:
            # heuristic 0 means the solution is correct
            return number_of_iterations, number_of_moves

        # otherwise find the highest scoring heuristic and make it better
        worst_score, worst_score_index = max((v,i) for (i,v) in enumerate(scores))
        worst_score_value = columns[worst_score_index]
        for a in range(size):
            if a == worst_score_value: continue
            c = index_value_score(worst_score_index, a)
            if c < worst_score:
                columns[worst_score_index] = a; number_of_moves += 1
                break
        else:
            # if there is no way to improve the worst performing heuristic
            # create a new board randomly
            if columns[0] & 1:
                random.shuffle(columns)
            else:
                place_n_queens(size)
            number_of_moves += 8

def index_value_score(i0: int, a: int) -> int:
    # gets the heurstic for a single queen
    count = 0
    for (i1, b) in enumerate(columns):
        if i0 == i1: # its the same number
            continue
        if a == b:
            count += 1
        elif abs(i0 - i1) == abs(a - b):
            count += 1
    return count


def hscore() -> list[int]:
    # returns a list where each index maps to the heuristic of each queen placement
    return [index_value_score(i0,a) for (i0, a) in enumerate(columns)]

def forward_checking(size: int) -> tuple[int, int]:
    # enums
    AVAILABLE, UNAVAILABLE, QUEEN = 0, 1, 2
    iterations, moves = 0, 0
    stack = [[[AVAILABLE] * size for _ in range(size)]]
    row = 0
    while row < size:
        iterations += 1
        # Is there an available spot for the queen?
        if choices := [i for (i, v) in enumerate(stack[-1][row]) if v == AVAILABLE]: 
            # YES!

            board = copy.deepcopy(stack[-1])
            # choose a random AVAILABLE spot for the queen
            col = random.choice(choices) # introduce a little anarchy
            board[row][col] = QUEEN
            moves += 1

            # black out the lower rows
            for (i, later_rows) in enumerate(range(row + 1, size), start=1):
                # block out lower vertical
                board[later_rows][col] = UNAVAILABLE
                # block out lower diagonals
                if col - i >= 0: board[later_rows][col - i] = UNAVAILABLE
                if col + i < size: board[later_rows][col + i] = UNAVAILABLE
            
            stack.append(board)
            row += 1
        else:
            # NO!
            # we mark the queens location in the prior row as unavailable
            row -= 1    
            queen_index = stack.pop()[row].index(QUEEN)
            stack[-1][row][queen_index] = UNAVAILABLE

    # convert the final board into the file standard format representation
    columns.clear()
    for row in stack.pop():
        columns.append(row.index(QUEEN))

    return iterations, moves

def eprint(*args, **kwargs):
    print(
        *args, **kwargs,
        # file=stderr,
    )

from time import time

# iters = 100
# size = 25
# print("method.__name__, avg_time, avg_moves, avg_iterations")
# for method in (heuristic_stochastic, forward_checking):
#     total_time = 0
#     total_moves = 0
#     total_iterations = 0
#     for i in range(iters):
#         start = time()
#         num_iterations, number_moves = method(size)
#         end = time()
#         total_time += (end - start)
#         total_moves += number_moves
#         total_iterations += num_iterations
#     print(method.__name__, total_time/iters, total_moves/iters, total_iterations/iters, sep=",")
# exit()

for method, m in (
    (dfs,26),
    (british_museum,11),
    (heuristic_stochastic,26),
    (forward_checking, 41),
):
    eprint(method.__name__)
    eprint("n,number_of_iterations,number_of_moves,time")
    for i in range(4,m):
        size = i

        start = time()
        num_iterations, number_moves=method(size)
        end = time()
        assert correct()

        eprint(size, num_iterations, number_moves, end - start, sep=',')
    eprint()

"""Now what?  Can you implement the British Museum Algorithm?  How many moves and iterations did it take to solve the 4 queens problem?  

How many moves/iterations did it take to solve the 8 queens (if at all)?
"""
"""
It is clear that foward checking is optimal relative to all other solutions in this file.
foward_checking(40) was less than dfs(25), british_museum(10), and heuristic_stochastic(25)
"""
"""
STDOUT Output:
dfs
n,number_of_iterations,number_of_moves,time
4,31,8,2.3126602172851562e-05
5,16,5,9.298324584960938e-06
6,197,31,7.081031799316406e-05
7,45,9,1.5974044799804688e-05
8,982,113,0.0003299713134765625
9,366,41,0.00012493133544921875
10,1068,102,0.0003781318664550781
11,559,52,0.0002009868621826172
12,3316,261,0.001260995864868164
13,1464,111,0.0005576610565185547
14,28381,1899,0.01174020767211914
15,21625,1359,0.009139060974121094
16,170749,10052,0.07598185539245605
17,96580,5374,0.043519020080566406
18,784511,41299,0.37198805809020996
19,50711,2545,0.02329397201538086
20,4192126,199635,2.103085994720459
21,188134,8562,0.09148073196411133
22,39955072,1737188,20.845487117767334
23,609997,25428,0.30259108543395996
24,10289901,411608,5.384507894515991
25,1265434,48683,0.6442201137542725

british_museum
n,number_of_iterations,number_of_moves,time
4,49,392,0.00013327598571777344
5,80,640,0.0001800060272216797
6,3633,29064,0.008878707885742188
7,4323,34584,0.011750936508178711
8,233426,1867408,0.8234782218933105
9,300726,2405808,1.1548640727996826
10,9376136,75009088,38.570860862731934

heuristic_stochastic
n,number_of_iterations,number_of_moves,time
4,19,75,0.00011491775512695312
5,3,10,1.7881393432617188e-05
6,77,217,0.0005676746368408203
7,38,108,0.0003497600555419922
8,13,27,0.00014066696166992188
9,32,74,0.00046062469482421875
10,239,526,0.003962993621826172
11,418,880,0.007823944091796875
12,1169,2408,0.025594711303710938
13,1415,2843,0.03582477569580078
14,1029,1974,0.029407978057861328
15,123,214,0.0038919448852539062
16,1767,3132,0.06318092346191406
17,7899,13877,0.31516504287719727
18,14299,24309,0.6289761066436768
19,9312,15395,0.45045995712280273
20,48171,78159,2.5552968978881836
21,23427,37329,1.3529720306396484
22,1849,2920,0.11641192436218262
23,17012,26133,1.155679702758789
24,41957,63776,3.08292818069458
25,56910,84903,4.499792098999023

forward_checking
n,number_of_iterations,number_of_moves,time
4,4,4,0.00011897087097167969
5,5,5,6.508827209472656e-05
6,50,28,0.0004591941833496094
7,21,14,0.00026798248291015625
8,10,9,0.00020885467529296875
9,139,74,0.002166748046875
10,54,32,0.0010941028594970703
11,399,205,0.007980823516845703
12,872,442,0.019635915756225586
13,23,18,0.0009310245513916016
14,122,68,0.0039000511169433594
15,475,245,0.01580500602722168
16,164,90,0.006505012512207031
17,105,61,0.00498199462890625
18,1302,660,0.05943012237548828
19,167,93,0.00915384292602539
20,626,323,0.03491806983947754
21,331,176,0.021021127700805664
22,2280,1151,0.14725017547607422
23,227,125,0.017346620559692383
24,914,469,0.07020688056945801
25,847,436,0.07083916664123535
26,154,90,0.01583385467529297
27,5921,2974,0.5574719905853271
28,498,263,0.05288505554199219
29,73,51,0.011011123657226562
30,34,32,0.007389068603515625
31,325,178,0.04292583465576172
32,1766,899,0.2298128604888916
33,417,225,0.06138801574707031
34,488,261,0.07567715644836426
35,131,83,0.025455951690673828
36,14460,7248,2.377383232116699
37,6319,3178,1.0780420303344727
38,492,265,0.09482288360595703
39,4241,2140,0.8106319904327393
40,520,280,0.1115870475769043



foward checking vs. hill climbing

100 trials, size 25

method.__name__, avg_time, avg_moves, avg_iterations
heuristic_stochastic,9.453199474811553,177896.59,119105.97
forward_checking,0.09797350883483887,597.98,1170.96

as we can clearly see, foward checking demolishes hill climbing
"""
