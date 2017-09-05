import yaml

import renderer.processing
import selector


if __name__ == '__main__':
    with open('dailygo.yaml', 'r') as f:
        config = yaml.load(f)

    #wallpaper_renderer = render.WallpaperRenderer(config)
    wallpaper_renderer = renderer.processing.ProcessingRenderer(config)
    sgf_selector = selector.FileSelector(config)
    wallpaper_renderer.save(position=sgf_selector.get_board())
