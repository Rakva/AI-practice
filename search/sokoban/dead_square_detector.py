#!/usr/bin/env python3
from game.board import Board, ETile
from typing import List


def detect(board: Board) -> List[List[bool]]:
    initial_array = []
    goals = []
    for y in range(board.height):
        row = []
        for x in range(board.width):
            tile = board.tile(x, y)
            if ETile.is_wall(tile):
                row.append("#")
            elif ETile.is_target(tile):
                row.append(".")
                goals.append((x,y))
            else:
                row.append(" ")
        initial_array.append(row)

    array = [[True for _ in range(board.height)] for _ in range(board.width)]
    while len(goals):
        temp_goal = []
        for element in goals:
            x = element[0]
            y = element[1]
            if not array[x][y]:
                continue

            array[x][y] = False

            if x - 1 >= 1 and x-2 >= 1:
                if not ETile.is_wall(board.tile(x - 1, y)) and not ETile.is_wall(board.tile(x - 2, y)):
                    temp_goal.append((x-1,y))
            if y - 1 >= 1 and y-2 >= 1:
                if not ETile.is_wall(board.tile(x , y-1)) and not ETile.is_wall(board.tile(x, y - 2)):
                    temp_goal.append((x,y-1))
            if x + 1 < board.width and x+2 <= board.width:
                if not ETile.is_wall(board.tile(x + 1, y)) and not ETile.is_wall(board.tile(x + 2, y)):
                    temp_goal.append((x+1,y))
            if y + 1 <= board.height and y + 2 <= board.height:
                if not ETile.is_wall(board.tile(x, y+1)) and not ETile.is_wall(board.tile(x, y + 2)):
                    temp_goal.append((x,y+1))
        goals = temp_goal
    return array
"""
    Returns 2D matrix containing true for dead squares.

    Dead squares are squares, from which a box cannot possibly
     be pushed to any goal (even if Sokoban could teleport
     to any location and there was only one box).

    You should prune the search at any point
     where a box is pushed to a dead square.

    Returned data structure is
        [board_width] lists
            of [board_height] lists
                of bool values.
    (This structure can be indexed "struct[x][y]"
     to get value on position (x, y).)
    """