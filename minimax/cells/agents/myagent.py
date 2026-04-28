#!/usr/bin/env python3
from game.agent import Agent
from game.cells import *
from sys import path
from os.path import dirname
from collections import deque
from typing import List, Union, Optional, Dict
from random import Random

path.append(dirname(dirname(dirname(__file__))))

class SafeMove(TransferMove):
    def add_transfer(self, transfer: Transfer) -> None:
        if all(transfer.source != t.source or transfer.target == t.target for t in self.transfers):
            self.add_and_combine_transfer(transfer)

class MyAgent(Agent):
    ATTACK_MUL = 0.8125

    def init_random(self, seed: Union[int, None]) -> None:
        self.random = Random(seed)

    def can_win(self, attack_mass: int, defend_mass: int) -> bool:
        return (attack_mass * self.ATTACK_MUL) > defend_mass

    def get_shortest_paths(self, cells: List[Cell]):
        n = len(cells)
        idx_map = {c.index: i for i, c in enumerate(cells)}
        paths = [[None] * n for _ in range(n)]

        for start_pos in range(n):
            q = deque([start_pos])
            paths[start_pos][start_pos] = [start_pos]
            while q:
                u = q.popleft()
                for nb in cells[u].neighbors:
                    v = idx_map[nb.index]
                    if paths[start_pos][v] is None:
                        paths[start_pos][v] = paths[start_pos][u] + [v]
                        q.append(v)
        return paths, idx_map

    def generate_full_move(self, game: Game, me: int) -> SafeMove:
        move = SafeMove()
        cells = game.cells
        my_cells = game.get_player_cells(me)
        paths, idx = self.get_shortest_paths(cells)

        incoming_est: Dict[int, int] = {c.index: 0 for c in cells}

        sent_source: Dict[int, bool] = {c.index: False for c in my_cells}

        def available_for(cell: Cell) -> int:
            total_after_incoming = cell.mass + incoming_est.get(cell.index, 0)
            safe_av = CellType.get_mass_over_min_size(total_after_incoming)
            cap = max(0, cell.mass - 1)  # cannot send more than current mass - 1
            return max(0, min(safe_av, cap))

        def plan_transfer(src: Cell, dst: Cell, amount: int) -> bool:
            if amount <= 0:
                return False
            if sent_source.get(src.index, False):
                return False
            if amount > available_for(src):
                return False
            move.add_transfer(Transfer(src, dst, amount))
            sent_source[src.index] = True
            incoming_est[dst.index] = incoming_est.get(dst.index, 0) + amount
            return True

        for cell in my_cells:
            avail = available_for(cell)
            if avail <= 0:
                continue

            neutral_neighbors = sorted([nb for nb in cell.neighbors if nb.owner == 0], key=lambda x: x.mass)
            acted = False
            for nb in neutral_neighbors:
                required = int(nb.mass / self.ATTACK_MUL) + 1
                # Only attempt if we can guarantee win with current availability
                if self.can_win(avail, nb.mass):
                    if plan_transfer(cell, nb, required):
                        acted = True
                        break
            if acted:
                continue

            enemy_neighbors = [nb for nb in cell.neighbors if nb.owner not in (0, me)]
            enemy_neighbors = sorted(enemy_neighbors, key=lambda x: x.mass)
            for nb in enemy_neighbors:
                if self.can_win(avail, nb.mass):
                    if plan_transfer(cell, nb, avail):
                        acted = True
                        break
            if acted:
                continue

            frontier = [c for c in my_cells if any(nb.owner != me for nb in c.neighbors)]
            if frontier:
                best_path = None
                best_dist = float('inf')
                ci = idx[cell.index]
                for f in frontier:
                    p = paths[ci][idx[f.index]]
                    if p and len(p) < best_dist:
                        best_dist = len(p)
                        best_path = p
                if best_path and len(best_path) >= 2:
                    nxt = cells[best_path[1]]
                    # send what we can (but not 0)
                    if plan_transfer(cell, nxt, avail):
                        continue

        return move

    def get_move(self, game: Game) -> List[Transfer]:
        return self.generate_full_move(game, game.current_player).get_transfers()
