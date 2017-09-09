import datetime
import os.path

import yaml

from pymainichigo.desktop import set_wallpaper
import pymainichigo.renderer.processing
import pymainichigo.selector


def compute_progress(sgf_selector):
    now = datetime.datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    day_progress = seconds_since_midnight / 86400.0
    sgf_progress = sgf_selector.get_game_length() * day_progress
    return sgf_progress

def main():
    with open(os.path.expanduser('~/.pymainichigo/dailygo.yaml'), 'r') as f:
        config = yaml.load(f)

    #wallpaper_renderer = render.WallpaperRenderer(config)
    wallpaper_renderer = pymainichigo.renderer.processing.ProcessingRenderer(config)
    sgf_selector = pymainichigo.selector.FileSelector(config)
    wallpaper_renderer.save(*sgf_selector.get_board(max_move_num=compute_progress(sgf_selector)))

    set_wallpaper(os.path.expanduser('~/.pymainichigo/wallpaper.png'))


if __name__ == '__main__':
    main()
