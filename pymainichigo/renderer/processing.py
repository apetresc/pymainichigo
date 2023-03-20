import glob
import os
import os.path
import re
import shutil
import subprocess
import tempfile

from jinja2 import Environment, PackageLoader
from xvfbwrapper import Xvfb


class ProcessingRenderer(object):
    def __init__(self, width, height, output_path, config):
        ProcessingRenderer._check_processing__()
        self.width, self.height = width, height
        self.template = Environment(loader=PackageLoader('pymainichigo', ''))\
            .get_template('goban.pde.template')
        self.output_path = output_path
        self.magnification = float(config.get('magnification', 5))
        self.color = config.get('color', '#826904')
        assert re.match(r'^#[A-Fa-f0-9]{6}$', self.color), f"Invalid color code: {self.color}"

    @staticmethod
    def _check_processing__():
        cmd = ['processing-java', '--help']
        with open(os.devnull, 'w') as null:
            r = subprocess.call(cmd, stdout=null, stderr=null)
        if r != 0:
            raise EnvironmentError("Cannot execute processing-java, make sure it is installed!")

    @staticmethod
    def _convert_position(board):
        symbols = [' ', '#', 'O']
        r = ''
        for i in range(1, len(board)):
            r += '  "'
            for j in range(1, len(board[i])):
                r += symbols[board[j][i]]
            r += '",\n'
        return r.rstrip(',')

    def save(self, position, last_move):
        with tempfile.TemporaryDirectory() as d:
            os.mkdir('%s/goban' % d)
            with open(os.path.join(d, 'goban', 'goban.pde'), mode='w') as f:
                f.write(self.template.render(
                    width=self.width,
                    height=self.height,
                    gridSizeQuotient=(40 - self.magnification * 2),
                    color=self.color,
                    position=ProcessingRenderer._convert_position(position),
                    last_x=last_move[0] - 1,
                    last_y=last_move[1] - 1))
            with Xvfb(width=1024, height=768, colordepth=24), open(os.devnull, 'w') as null:
                cmd = ['processing-java', f'--sketch={d}/goban', '--run']
                subprocess.call(cmd, stdout=null, stderr=null)
            shutil.copy(os.path.join(d, 'goban', 'wallpaper.png'), os.path.expanduser(self.output_path))
        list(map(shutil.rmtree, glob.glob(os.path.join(tempfile.gettempdir(), 'goban*temp'))))
