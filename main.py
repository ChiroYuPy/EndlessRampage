# main.py
import pygame
from src.game.game import Game


def main():
    pygame.init()

    game = Game()
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
