#!/usr/bin/env python3
from search_templates import Problem, Solution
from typing import Optional
import heapq
import itertools

def ucs(prob: Problem) -> Optional[Solution]:
    """Return Solution of the problem solved by UCS search."""

    counter = itertools.count()  # unique sequence count
    frontier = [(0, next(counter), prob.initial_state(), [prob.initial_state()])]  # (cost, state, path)
    visited = {}  # state -> best known cost

    while frontier:
        total_cost, _, state,  path = heapq.heappop(frontier)

        # print(frontier)
        if prob.is_goal(state):
            return Solution(path[1:], state, total_cost)

        if state in visited and visited[state] <= total_cost:
            continue

        visited[state] = total_cost

        for action in prob.actions(state):
            new_state = prob.result(state, action)
            cost = prob.cost(state, action)
            heapq.heappush(frontier, (int(total_cost + cost), next(counter), new_state, path + [action]))

    return None
