from collections import defaultdict
import sys

from PIL import Image
import sgf

from gogame import GoGame


class GobanRenderer(object):
    """
    board -> GoGame.contents
    img -> Pillow image to draw into
    config -> YAML config with some settings
    """
    def draw_board(board, img, config):
        pass


class WallpaperRenderer(object):
    def __init__(self, config):
        self.width, self.height = config['wallpaper']['width'], config['wallpaper']['height']
        self.goban_width, self.goban_height = self._calculate_goban_dimensions(config)

        self.image = Image.new(mode='RGB', size=(self.width, self.height))

    def render(self):
        pass

    def save(self):
        self.image.save('wallpaper.png')


class SimpleRenderer(WallpaperRenderer):
    def _calculate_goban_dimensions(self, config):
        return self.height * 0.8, self.height * 0.8



def draw_board(board):
    symbols = ['.', '#', 'O']
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(symbols[board[i][j]], end=' ')
        print('')
