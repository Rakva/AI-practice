#!/usr/bin/env python3
from game.action import *
from game.board import *
from game.artificial_agent import ArtificialAgent
from dead_square_detector import detect
from typing import List, Union
import sys
from time import perf_counter
from os.path import dirname
import numpy as np

sys.path.append(dirname(dirname(dirname(__file__))))
from astar import AStar
from search_templates import HeuristicProblem


class MyAgent(ArtificialAgent):

    def __init__(self, optimal, verbose) -> None:
        super().__init__(optimal, verbose)  # recommended

    def new_game(self) -> None:
        super().new_game()  # recommended

    @staticmethod
    def think(
            board: Board, optimal: bool, verbose: bool
    ) -> List[Union[EDirection, Action]]:

        prob = SokobanProblem(board)
        solution = AStar(prob)
        if not solution:
            return None
        return [a.dir for a in solution.actions]


class SokobanProblem(HeuristicProblem):

    def __init__(self, board) -> None:
        self.init = board
        self.dead_squares = detect(board)
        self.goals = []
        x = 0
        while x < board.height:
            y = 0
            while y < board.width:
                if board.tile(y, x) == 1 or board.tile(y, x) == 3 or board.tile(y, x) == 5:
                    self.goals.append([x, y])
                y = y + 1
            x = x + 1
        # precompute manhattan distances for all (x,y) to each goal
        grid_x, grid_y = np.meshgrid(np.arange(board.width),
                                     np.arange(board.height))
        # shape: (height, width)
        self.goal_maps = [
            np.abs(grid_x - gx) + np.abs(grid_y - gy)
            for gx, gy in self.goals
        ]
        # stack into array for vectorized min later
        self.goal_maps = np.stack(self.goal_maps, axis=0)


    def initial_state(self) -> Union[Board, StateMinimal]:

        return self.init

    def actions(self, state: Union[Board, StateMinimal]) -> List[Action]:
        actions = []
        for m in Move.get_actions():
            if m.is_possible(state):
                actions.append(m)
        for p in Push.get_actions():
            if p.is_possible(state):
                actions.append(p)
        return actions

    def result(
            self, state: Union[Board, StateMinimal], action: Action
    ) -> Union[Board, StateMinimal]:

        copy_state = state.clone()
        action.perform(copy_state)
        return copy_state

    def is_goal(self, state: Union[Board, StateMinimal]) -> bool:
        return state.is_victory()

    def cost(self, state: Union[Board, StateMinimal], action: Action) -> float:
        return 1

    def estimate(self, state: Union[Board, StateMinimal]) -> float:

        # collect box coordinates (list comprehension faster than nested loops)
        boxes = [(x, y)
                 for x in range(state.height)
                 for y in range(state.width)
                 if state.tile(y, x) in (2, 3)]

        if not boxes:
            return 0.0

        total = 0
        for bx, by in boxes:
            # deadlock check
            if self.dead_squares[by][bx]:
                return float('inf')
            # vectorized lookup: distances to all goals
            dists = self.goal_maps[:, by, bx]
            total += np.min(dists)

        return float(total)

