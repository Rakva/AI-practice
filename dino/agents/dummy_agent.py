#!/usr/bin/env python3
from game.dino import *
from game.agent import Agent


class Dummy_Agent(Agent):
    """Reflex agent static class for Dino game."""

    # use class variables only for debugging
    debug_txt = None

    def __init__(self) -> None:
        # AGENT WON'T BE INITIALIZED, SO THIS IS FINE
        raise RuntimeError

    @staticmethod
    def get_move(game: Game) -> DinoMove:
        if Dummy_Agent.debug:
            from game.debug_game import DebugGame

            game: DebugGame = game
            if Dummy_Agent.debug_txt is None:
                _ = game.add_text(Coords(10, 10), "red", "Hello World.")
                Dummy_Agent.debug_txt = game.add_text(
                    Coords(10, 30), "red", "0"
                )
            else:
                Dummy_Agent.debug_txt.text = str(game.score)
            game.add_dino_rect(Coords(-10, -10), 150, 150, "yellow")
            l = game.add_dino_line(
                Coords(0, 0), Coords(600 // game.speed, 0), "black"
            )
            l.vector.x -= Dino.HEAD_X + game.dino.head.width
            l.dxdy.update(Dino.HEAD_X + game.dino.head.width, 0)
            l.dxdy.y += 50
            if game.score % 20 == 0:
                game.add_moving_line(
                    Coords(1000, 100), Coords(1000, 500), "purple"
                )

        # Dummy implementation:
        x = game.dino.x

        bird2 = False
        i = 0
        first_o_x = 0
        second_o_x = 0
        size = 0
        for o in game.obstacles:
            size= size+1
        print(size)
        for o in game.obstacles:
            i = i+1
            if i == 1:
                first_o_x = o.rect.x

            if i == 2:
                second_o_x = o.rect.x

            #while under the bird on the highest level
            if i==1 and bird2 and o.rect.x > x:
                return DinoMove.DOWN

            if o.type.name == "BIRD2" and o.rect.x - x - game.dino.HEAD_X < 100:
                bird2 = True
                return DinoMove.DOWN
            bird2 = False

            #while in the air to jump on the second obstacle too
            if second_o_x > x > first_o_x and second_o_x - first_o_x < 200:
                return DinoMove.UP_RIGHT

            #to avoid obstacle based on height
            if o.rect.y > 290 and o.rect.x - x - game.dino.HEAD_X < 150 + 5 * (game.speed - o.speed - 5):

                if o.rect.x + o.rect.width - o.speed * 5 > x:

                    # if Dummy_Agent.verbose:
                    #     print("jumping right")
                    return DinoMove.UP_RIGHT

                if o.rect.x + o.rect.width < x:
                    # if Dummy_Agent.verbose:
                    #     print("jumping right")
                    return DinoMove.DOWN

            if o.rect.y < 290 and  o.rect.x - x - game.dino.HEAD_X < 150 + 5 * (game.speed - o.speed - 5):

                if o.rect.x + o.rect.width - o.speed * 5 > x:

                    # if Dummy_Agent.verbose:
                    #     print("jumping right")
                    return DinoMove.DOWN

            if o.rect.x < x and o.rect.x - x > 40:

                # if Dummy_Agent.verbose:
                #     print("running right")
                return DinoMove.DOWN_RIGHT



        return DinoMove.NO_MOVE
