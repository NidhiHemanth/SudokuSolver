import os
from time import sleep


def screen_clear():
    _ = os.system('cls')

# sleep(5)
# screen_clear()


board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def print_board(bo):

    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("-----------------------")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")

            if j == 8:
                print(bo[i][j])
            elif j == 0:
                print(" "+str(bo[i][j])+" ", end="")
            else:
                print(str(bo[i][j])+" ", end="")
    return ""


def find_empty(bo):

    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)

    return None                                           # None is a False type

# to check if the current board is valid


def valid(bo, num, pos):                                  # pos = (i,j)

    # checking row, iterate over each column of the element row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # checking column, iterate over each row of the element column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # which box has the element?
    box_x = pos[0] // 3
    # eg (2,6) has box_x = 0, box_y = 2
    box_y = pos[1] // 3

    for i in range(box_x*3, box_x*3 + 3):
        for j in range(box_y*3, box_y*3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

# backtrack algorithm


def solve(bo):

    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, find):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


solve(board)
sleep(5)
screen_clear()
print_board(board)
