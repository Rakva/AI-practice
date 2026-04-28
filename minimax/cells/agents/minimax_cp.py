from minimax_templates import *

class Minimax(Strategy):

    def __init__(self, game: HeuristicGame, limit: int = 0, seed: Optional[int] = None) -> None:
        super().__init__(seed)
        self.game = game
        self.limit = limit  # 0 means unlimited depth


    def action(self, state):
        root_player = self.game.player(state)
        depth_limit = None if self.limit == 0 else self.limit

        best_value = float("-inf")
        best_action = None
        alpha = float("-inf")
        beta = float("inf")

        for action in self.game.actions(state):
            ns = self.game.clone(state)
            self.game.apply(ns, action)

            value = self._minimax(
                ns,
                depth=1,
                limit=depth_limit,
                alpha=alpha,
                beta=beta,
                root_player=root_player
            )

            if value > best_value:
                best_value = value
                best_action = action

            alpha = max(alpha, best_value)

        return best_action

    def _minimax(self, state, depth, limit, alpha, beta, root_player):

        # terminal state
        if self.game.is_done(state):
            outcome = self.game.outcome(state)

            relative = outcome if root_player == 1 else -outcome

            if relative == +1:
                return 10_000 - depth
            elif relative == -1:
                return -10_000 + depth
            else:
                return 0

        # cutoff by depth
        if limit is not None and depth >= limit:
            eval_value = self.game.evaluate(state)
            return eval_value if root_player == 1 else -eval_value

        current_player = self.game.player(state)

        if current_player == root_player:
            value = float("-inf")
            for action in self.game.actions(state):
                ns = self.game.clone(state)
                self.game.apply(ns, action)
                value = max(value, self._minimax(ns, depth+1, limit, alpha, beta, root_player))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        else:
            value = float("inf")
            for action in self.game.actions(state):
                ns = self.game.clone(state)
                self.game.apply(ns, action)
                value = min(value, self._minimax(ns, depth+1, limit, alpha, beta, root_player))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
