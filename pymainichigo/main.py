import datetime
import os
import os.path

import yaml

from pymainichigo.desktop import set_wallpaper
import pymainichigo.renderer.processing
import pymainichigo.selector


DEFAULT_CONFIG = {
    'wallpaper': {
        'output': '~/.pymainichigo/wallpaper.png',
        'width': 1920,
        'height': 1080
    },
    'sgf': {
        'file': os.path.join(os.path.dirname(__file__), 'test.sgf')
    }
}

def create_config(config_dir, config_file):
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            f.write(yaml.dump(DEFAULT_CONFIG))

def compute_progress(sgf_selector):
    now = datetime.datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    day_progress = seconds_since_midnight / 86400.0
    sgf_progress = sgf_selector.get_game_length() * day_progress
    return sgf_progress

def main():
    config_file = os.path.expanduser('~/.pymainichigo/config.yaml')
    config_dir = os.path.dirname(config_file)
    create_config(config_dir, config_file)

    with open(config_file, 'r') as f:
        config = yaml.load(f)

    wallpaper_renderer = pymainichigo.renderer.processing.ProcessingRenderer(config)
    sgf_selector = pymainichigo.selector.FileSelector(config)
    wallpaper_renderer.save(*sgf_selector.get_board(max_move_num=compute_progress(sgf_selector)))

    set_wallpaper(os.path.expanduser(config['wallpaper']['output']))


if __name__ == '__main__':
    main()
