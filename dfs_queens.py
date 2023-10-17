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

def solve_queen(size):
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
        print(number_of_moves)
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
                print("I did it! Here is my solution")
                display()
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            if (prev_column == -1): #I backtracked past column 1
                print("There are no solutions")
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
    place_n_queens(size)
    count = 1
    while not correct():
        place_n_queens(size)
        count += 1
    return count, count * 8

def hrss(size: int) -> tuple[int, int]:
    number_of_moves = 0 #where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0
    place_n_queens(size); number_of_moves += 8
    while True:
        number_of_iterations += 1
        scores = hscore()
        total_score = sum(scores)
        if total_score == 0:
            # you found something
            return number_of_iterations, number_of_moves
        # find the worst spot and kill it
        worst_score, worst_score_index = max((v,i) for (i,v) in enumerate(scores))
        worst_score_value = columns[worst_score_index]
        for a in range(size):
            if a == worst_score_value: continue
            c = index_value_score(worst_score_index, a)
            if c < worst_score:
                columns[worst_score_index] = a; number_of_moves += 1
                break
        else:
            if columns[0] & 1:
                random.shuffle(columns)
            else:
                place_n_queens(size)
            number_of_moves += 8

def index_value_score(i0: int, a: int) -> int:
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
    return [index_value_score(i0,a) for (i0, a) in enumerate(columns)]


from time import time

for method, m in (
    (solve_queen,18),
    (british_museum,9),
    (hrss,41),
):
    print(method.__name__ , file=stderr)
    print("n,number_of_iterations,number_of_moves,time", file=stderr)
    for i in range(4,m):
        #size = int(input('Enter n: '))
        size = i
        num_iterations=0
        number_moves = 0
        #for i in range(0, 100):
        #    columns = [] #columns is the locations for each of the queens
        start = time()
        num_iterations, number_moves=method(size)
        end = time()
        # edisplay()
        # print(num_iterations)
        # print(number_moves)
        # print(columns)
        print(size, num_iterations, number_moves, end - start, sep=',', file=stderr)
    print(file=stderr)

"""Now what?  Can you implement the British Museum Algorithm?  How many moves and iterations did it take to solve the 4 queens problem?  

How many moves/iterations did it take to solve the 8 queens (if at all)?
"""