import os
import os.path
import shutil
import subprocess
import tempfile

from jinja2 import Environment, PackageLoader
from xvfbwrapper import Xvfb


class ProcessingRenderer(object):
    def __init__(self, config):
        ProcessingRenderer._check_processing__()
        self.width, self.height = config['wallpaper']['width'], config['wallpaper']['height']
        self.template = Environment(loader=PackageLoader('pymainichigo', ''))\
            .get_template('goban.pde.template')
        self.output_path = config['wallpaper']['output']

    @staticmethod
    def _check_processing__():
        cmd = ['processing-java', '--help']
        r = subprocess.call(cmd)
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
        print("LAST MOVE: %s" % (last_move,))
        with tempfile.TemporaryDirectory() as d:
            os.mkdir('%s/goban' % d)
            with open(os.path.join(d, 'goban', 'goban.pde'), mode='w') as f:
                f.write(self.template.render(
                    width=self.width,
                    height=self.height,
                    position=ProcessingRenderer._convert_position(position),
                    last_x=last_move[0] - 1,
                    last_y=last_move[1] - 1))
            with open(os.path.join(d, 'goban', 'goban.pde'), mode='r') as f:
                print(f.read())
            with Xvfb(width=1024, height=768, colordepth=24):
                cmd = ['processing-java', '--sketch=%s/goban' % d, '--run']
                print("Calling %s" % ' '.join(cmd))
                subprocess.call(cmd)
            shutil.copy(os.path.join(d, 'goban', 'wallpaper.png'), os.path.expanduser(self.output_path))
