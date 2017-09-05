import os
import os.path
import shutil
import subprocess
import tempfile

from jinja2 import Environment, FileSystemLoader, Template
from xvfbwrapper import Xvfb


class ProcessingRenderer(object):
    def __init__(self, config):
        self.width, self.height = config['wallpaper']['width'], config['wallpaper']['height']
        self.template = Environment(loader=FileSystemLoader(searchpath='./'))\
                .get_template('goban.pde.template')

    @staticmethod
    def _convert_position(board):
        symbols = [' ', '#', 'O']
        r = ''
        for i in range(len(board)):
            r += '  "'
            for j in range(len(board[i])):
                r += symbols[board[i][j]]
            r += '",'
        return r.rstrip(',')



    def save(self, position):
        with tempfile.TemporaryDirectory() as d:
            os.mkdir('%s/goban' % d)
            with open(os.path.join(d, 'goban', 'goban.pde'), mode='w') as f:
                f.write(self.template.render(
                    width=self.width,
                    height=self.height,
                    position=ProcessingRenderer._convert_position(position)))
            with Xvfb(width=1024, height=768, colordepth=24) as xvfb:
                subprocess.call(['processing-java', '--sketch=%s/goban' % d, '--run'])
            shutil.copy(os.path.join(d, 'goban', 'wallpaper.png'), 'wallpaper.png')
