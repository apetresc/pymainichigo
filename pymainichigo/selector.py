import glob
import os.path
import random

import feedparser
import requests
import sgf

from pymainichigo.gogame import GoGame


class SgfSelector(object):
    def __init__(self, config):
        pass

    def write_to_cache(self, cache_file):
        with open(cache_file, 'w') as f:
            f.write(self.get_sgf())

    def get_sgf(self):
        raise NotImplementedError


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


class RssSelector(SgfSelector):
    def __init__(self, config):
        super(RssSelector, self).__init__(config)
        self.feed_url = config['feed_url']

    def _get_link(self):
        d = feedparser.parse(self.feed_url)
        return d['entries'][0]['link']

    def get_sgf(self):
        sgf_link = self._get_link()
        r = requests.get(sgf_link)
        if r.status_code == 200:
            return r.text
        else:
            raise RuntimeError("Could not download %s from RSS feed %s" % (sgf_link, self.feed_url))


class GoKifuSelector(RssSelector):
    FEED_URL = 'http://gokifu.com/rss/'

    def __init__(self, config):
        SgfSelector.__init__(self, config)
        self.feed_url = GoKifuSelector.FEED_URL

    def _get_link(self):
        return '%s.sgf' % super(GoKifuSelector, self)._get_link().replace('/s/', '/f/')


class SGF(object):
    def __init__(self, fn):
        self.fn = fn
        with open(self.fn, 'r') as f:
            collection = sgf.parse(f.read())
            self.game = collection.children[0]
            self.N = int(self.game.root.properties.get("SZ", ["19"])[0])

    def get_game_length(self):
        moves = 0
        for node in self.game:
            moves += 1
        return moves

    def get_board(self, max_move_num=100):
        board = GoGame(size=self.N, handicap=0)

        move_num = 0
        for node in self.game:
            move_num += 1
            move = node.properties.get("B") or node.properties.get("W")
            if move:
                move_coords = sgf.SGF_POS.index(move[0][0]), sgf.SGF_POS.index(move[0][1])
                board.move_stone(*move_coords)
                if move_num >= max_move_num:
                    break

        return board.contents, move_coords
