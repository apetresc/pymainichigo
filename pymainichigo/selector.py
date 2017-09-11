import glob
import os.path
import random

import feedparser
import requests


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
