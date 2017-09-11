import glob
import os.path
import random


class SgfSelector(object):
    def __init__(self, config):
        pass

    def write_to_cache(self, cache_file):
        with open(cache_file, 'w') as f:
            f.write(self.get_sgf())

    def get_sgf(self):
        raise NotImplemented


class FileSelector(SgfSelector):
    def __init__(self, config):
        super(FileSelector, self).__init__(config)
        self.fn = os.path.expanduser(config['path'])

    def get_sgf(self):
        with open(self.fn, 'r') as f:
            return f.read()


class DirSelector(SgfSelector):
    def __init__(self, config):
        super(DirSelector, self).__init__(config)
        self.dir = os.path.expanduser(config['path'])

    def get_sgf(self):
        all_sgfs = glob.glob(os.path.join(self.dir, '**/*.sgf'), recursive=True)
        with open(all_sgfs[random.randint(0, len(all_sgfs) - 1)], 'r') as f:
            return f.read()
