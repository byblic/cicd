import pygame
import sys
import random
import math
import argparse

pygame.init()

# Initialize sound variables
eat_sound = pygame.mixer.Sound("./sounds/collect.wav")
lose_sound = pygame.mixer.Sound("./sounds/lose.wav")
win_sound = pygame.mixer.Sound("./sounds/win.wav")

# Initialize font
font = pygame.font.Font(None, 36)

# Constants
CELL_SIZE = 40
GRID_WIDTH = 15
GRID_HEIGHT = 15
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (80, 80, 80)
VIOLET = (151, 89, 154)

class GameSettings:
    def __init__(self):
        self.difficulty = 'medium'
        self.bg_color = 'black'
        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Pac-Man Game Settings")
        parser.add_argument('--difficulty', type=str, choices=['easy', 'medium', 'hard'], default='hard', help="Set the game difficulty")
        parser.add_argument('--bg_color', type=str, choices=['black', 'pink', 'gray'], default='pink', help="Set the background color")
        args = parser.parse_args()
        self.difficulty = args.difficulty
        self.bg_color = args.bg_color

        # Set delays based on difficulty
        global pacman_move_delay, ghost_move_delay, mouth_anim_delay
        if self.difficulty == 'easy':
            pacman_move_delay = 200
            ghost_move_delay = 500
            mouth_anim_delay = 600
        elif self.difficulty == 'medium':
            pacman_move_delay = 150
            ghost_move_delay = 400
            mouth_anim_delay = 500
        else:  # 'hard' 
            pacman_move_delay = 100
            ghost_move_delay = 300
            mouth_anim_delay = 400

        # Set background color
        global BG_COLOR
        if self.bg_color == 'pink':
            BG_COLOR = PINK
        elif self.bg_color == 'gray':
            BG_COLOR = GRAY
        else:  # 'default(black)'
            BG_COLOR = BLACK
