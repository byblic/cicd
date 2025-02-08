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

class PacMan:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.direction = 3  # 0: right, 1: down, 2: left, 3: up
        self.mouth_open = False

    def move(self, grid, score, game_state):
        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][self.direction]
        new_x, new_y = self.x + dx, self.y + dy
        if grid[new_y][new_x] != 1:
            self.x, self.y = new_x, new_y
            if grid[new_y][new_x] == 0:
                grid[new_y][new_x] = 2  # Mark as eaten
                score += 10
                SoundManager.play_eat_sound()
                if all(cell != 0 for row in grid for cell in row):
                    game_state = GameState.GAME_WIN
                    SoundManager.play_win_sound()
        return score, game_state

    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 50
        mouth_opening = 45 if self.mouth_open else 0
        pygame.draw.circle(screen, YELLOW, (x, y), CELL_SIZE // 2)
        if self.direction == 0:  # Right
            start_angle = 360 - mouth_opening / 2
            end_angle = mouth_opening / 2
        elif self.direction == 3:  # Down
            start_angle = 90 - mouth_opening / 2
            end_angle = 90 + mouth_opening / 2
        elif self.direction == 2:  # Left
            start_angle = 180 - mouth_opening / 2
            end_angle = 180 + mouth_opening / 2
        else:  # Ups
            start_angle = 270 - mouth_opening / 2
            end_angle = 270 + mouth_opening / 2
        pygame.draw.arc(screen, BLACK, (x - CELL_SIZE // 2, y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE), math.radians(start_angle), math.radians(end_angle), CELL_SIZE // 2)
        mouth_line_end_x = x + math.cos(math.radians(start_angle)) * CELL_SIZE // 2
        mouth_line_end_y = y - math.sin(math.radians(start_angle)) * CELL_SIZE // 2
        pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)
        mouth_line_end_x = x + math.cos(math.radians(end_angle)) * CELL_SIZE // 2
        mouth_line_end_y = y - math.sin(math.radians(end_angle)) * CELL_SIZE // 2
        pygame.draw.line(screen, BLACK, (x, y), (mouth_line_end_x, mouth_line_end_y), 2)
