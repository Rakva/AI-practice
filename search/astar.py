#!/usr/bin/env python3
from search_templates import Solution, HeuristicProblem
import heapq
import itertools
import math

class Node:
    def __init__(self, state, parent=None, action_step=None, path_cost=0, h_cost=0):
        self.state = state
        self.parent = parent
        self.action_step = action_step
        self.path_cost = path_cost
        self.h_cost = h_cost
        self.overall_cost = path_cost + h_cost

    def __lt__(self, other):
        return self.overall_cost < other.overall_cost

def AStar(prob):


    start = prob.initial_state()
    start_node = Node(start, path_cost=0, h_cost=prob.estimate(start))

    frontier = []
    heapq.heappush(frontier, start_node)

    explored = {}
    explored[start] = 0
    while frontier:
        current_node = heapq.heappop(frontier)
        current_state = current_node.state

        if prob.is_goal(current_state):
            actions = []
            goal_state = current_node.state
            path_cost = current_node.path_cost

            while current_node.parent is not None:
                actions.append(current_node.action_step)
                current_node = current_node.parent
            actions.reverse()

            return Solution(actions, goal_state, path_cost)


        for action_step in prob.actions(current_state):
            new_state = prob.result(current_state, action_step)
            path_cost = current_node.path_cost + prob.cost(current_state, action_step)
            h_cost = prob.estimate(new_state)

            if new_state not in explored or path_cost < explored[new_state]:

                explored[new_state] = path_cost
                new_node = Node(new_state,
                                parent=current_node,
                                action_step=action_step,
                                path_cost=path_cost,
                                h_cost=h_cost)
                heapq.heappush(frontier, new_node)

    return Solution(None, None, float('inf'))
