import datetime
import math
import os
import os.path

import yaml

from pymainichigo.desktop import set_wallpaper
import pymainichigo.renderer.pillow
import pymainichigo.selector


DEFAULT_CONFIG = yaml.load("""
wallpaper:
  output: "~/.pymainichigo/wallpaper.png"
  width: 1920
  height: 1080
curve: linear
sgf:
  file:
    path: "{}"
render:
  pillow:
    color: "#826904"
sys:
  set_wallpaper: false
""", Loader=yaml.SafeLoader)
DEFAULT_CONFIG["sgf"]["file"]["path"] = os.path.join(os.path.dirname(__file__), 'test.sgf')


def create_config(config_dir, config_file):
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    if not os.path.exists(config_file):
        with open(config_file, 'w', encoding='utf8') as f:
            f.write(yaml.dump(DEFAULT_CONFIG, default_flow_style=False))
    if not os.path.exists(os.path.join(config_dir, 'cache')):
        os.mkdir(os.path.join(config_dir, 'cache'))


def compute_progress(sgf, curve):
    now = datetime.datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    day_progress = seconds_since_midnight / 86400.0

    if curve == 'linear':
        sgf_progress = sgf.get_game_length() * day_progress
    elif curve == 'sigmoid':
        sgf_progress = sgf.get_game_length() * (1 / (1 + math.exp(-12 * day_progress + 6)))
    else:
        raise RuntimeError(f"Invalid curve: {curve}")
    return sgf_progress


def main():
    config_file = os.path.expanduser('~/.pymainichigo/config.yaml')
    config_dir = os.path.dirname(config_file)
    create_config(config_dir, config_file)

    with open(config_file, 'r', encoding='utf8') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    sgf_path = os.path.expanduser(f"~/.pymainichigo/cache/{datetime.datetime.now().date()}.sgf")
    if not os.path.exists(sgf_path):
        for selector in config['sgf']:
            try:
                if selector == 'file':
                    sgf_selector = pymainichigo.selector.FileSelector(config['sgf'][selector])
                elif selector == 'dir':
                    sgf_selector = pymainichigo.selector.DirSelector(config['sgf'][selector])
                elif selector == 'rss':
                    sgf_selector = pymainichigo.selector.RssSelector(config['sgf'][selector])
                elif selector == 'gokifu':
                    sgf_selector = pymainichigo.selector.GoKifuSelector(config['sgf'][selector])
            except RuntimeError:
                continue
            break
        if sgf_selector:
            sgf_selector.write_to_cache(sgf_path)
        else:
            raise RuntimeError("No SGF selector was able to find an SGF")
    sgf = pymainichigo.selector.SGF(sgf_path)

    wallpaper_renderer = pymainichigo.renderer.pillow.PillowRenderer(
        config=config['render']['pillow'] or {},
        width=config['wallpaper']['width'],
        height=config['wallpaper']['height'],
        output_path=config['wallpaper']['output'])
    wallpaper_renderer.save(*sgf.get_board(max_move_num=compute_progress(sgf, config.get('curve', 'linear'))))
    if config['sys']['set_wallpaper']:
        set_wallpaper(os.path.expanduser(config['wallpaper']['output']))


if __name__ == '__main__':
    main()
