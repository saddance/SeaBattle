from game import Game
from players.human_player import Human_player
from players.advanced_player import Advanced_player


if __name__ == "__main__":
    game = Game()
    game.add_player(Human_player())
    game.add_player(Advanced_player())
    game.show_menu()
