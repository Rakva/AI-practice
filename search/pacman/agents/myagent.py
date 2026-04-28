#!/usr/bin/env python3
from game.controllers import PacManControllerBase
from game.pacman import Game, DM
import heapq

class PacProblem:
    def __init__(self, game: Game):
        self.game = game
        self.start = game.pac_loc
        pills = game.get_active_pills_nodes()
        power_pills = game.get_active_power_pills_nodes()
        self.goals = pills + power_pills
        for g in range(game.NUM_GHOSTS):
            if game.is_edible(g) and game.get_edible_time(g) > 45:
                self.goals.append(game.get_ghost_loc(g))

    def initial_state(self):
        return self.start

    def actions(self, state):
        return self.game.get_possible_dirs(state)

    def result(self, state, action):
        return self.game.get_neighbor(state, action)

    def is_goal(self, state):
        return state in self.goals

    def cost(self, state, action):
        new_state = self.result(state, action)
        cost = 1.0
        nearest_ghost_dist = float('inf')
        for g in range(self.game.NUM_GHOSTS):
            g_loc = self.game.get_ghost_loc(g)
            if g_loc is None or self.game.get_lair_time(g) > 0:
                continue
            dist = self.game.get_path_distance(new_state, g_loc)
            edible_time = self.game.get_edible_time(g)
            if not self.game.is_edible(g) or edible_time < 45:
                if dist < 8:
                    cost += (8 - dist) ** 3 * 50
            else:
                if edible_time > 40 and dist < 6:
                    cost += 0.2 * dist
                elif edible_time <= 20 and dist < 6:
                    cost += (6 - dist) ** 2 * 40
            nearest_ghost_dist = min(nearest_ghost_dist, dist)
        if nearest_ghost_dist < 6:
            for pp in self.game.get_active_power_pills_nodes():
                if new_state == pp:
                    cost *= 0.2
        return cost


def ucs(problem):
    start = problem.initial_state()
    frontier = [(0, start, [])]
    explored = set()
    while frontier:
        cost, state, path = heapq.heappop(frontier)
        if state in explored:
            continue
        explored.add(state)
        if problem.is_goal(state):
            return type("Solution", (), {"actions": path})
        for action in problem.actions(state):
            next_state = problem.result(state, action)
            if next_state not in explored:
                total_cost = cost + problem.cost(state, action)
                heapq.heappush(frontier, (total_cost, next_state, path + [action]))
    return None


class MyAgent(PacManControllerBase):
    def tick(self, game: Game) -> None:
        prob = PacProblem(game)
        sol = ucs(prob)
        if sol and sol.actions:
            self.pacman.set(sol.actions[0])
