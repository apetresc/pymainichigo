import datetime

import yaml

from desktop import set_wallpaper
import renderer.processing
import selector


def compute_progress(sgf_selector):
    now = datetime.datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    day_progress = seconds_since_midnight / 86400.0
    sgf_progress = sgf_selector.get_game_length() * day_progress
    return sgf_progress

if __name__ == '__main__':
    with open('dailygo.yaml', 'r') as f:
        config = yaml.load(f)

    #wallpaper_renderer = render.WallpaperRenderer(config)
    wallpaper_renderer = renderer.processing.ProcessingRenderer(config)
    sgf_selector = selector.FileSelector(config)
    wallpaper_renderer.save(*sgf_selector.get_board(max_move_num=compute_progress(sgf_selector)))

    set_wallpaper('wallpaper.png')
