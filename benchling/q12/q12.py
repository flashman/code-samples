"""
. Given a 2D array, print the items in a spiral.
print_spiral(
    [[ 1, 2, 3, 4],
    [ 5, 6, 7, 8],
    [ 9, 10, 11, 12],
    [13, 14, 15, 16]]
)
E.g. the above prints in the order of 1 2 3 4 8 12 16 15 14 13 9 5 6 7 11 10
"""


import numpy as np


def print_spiral(matrix):
    out = []
    matrix = np.array(matrix)

    while matrix.shape[0] > 0 and matrix.shape[1] > 0:
        out.extend(list(matrix[0, :]))
        matrix = np.rot90(matrix[1:, :])

    return out


def test_print_spiral_example():
    matrix_in = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]
    expected = [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10]
    assert expected == print_spiral(matrix_in)


def test_print_spiral_row():
    matrix_in = [
        [1, 2, 3, 4],
    ]
    expected = [1, 2, 3, 4]
    assert expected == print_spiral(matrix_in)


def test_print_spiral_col():
    matrix_in = [
        [1],
        [2],
        [3],
        [4],
    ]
    expected = [1, 2, 3, 4]
    assert expected == print_spiral(matrix_in)
