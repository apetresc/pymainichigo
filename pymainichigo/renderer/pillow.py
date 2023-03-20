import colorsys
import os
import random
from math import floor, sqrt

from PIL import Image, ImageDraw, ImageFilter


class PillowRenderer(object):

    def __init__(self, width, height, output_path, config):
        self.width, self.height = width, height
        self.output_path = os.path.expanduser(output_path)

        # Colors
        self.board_color = tuple(int(config.get('color', '#826904')[i:i+2], 16) for i in (1, 3, 5))
        board_color_hsv = colorsys.rgb_to_hsv(self.board_color[0] / 255.0, self.board_color[1] / 255.0, self.board_color[2] / 255.0)
        self.white_color = tuple(map(lambda x: int(x * 255.0), colorsys.hsv_to_rgb(board_color_hsv[0], board_color_hsv[1] / 2, (board_color_hsv[2] + 2) / 3)))
        self.black_color = tuple(map(lambda x: int(x * 255.0), colorsys.hsv_to_rgb(board_color_hsv[0], board_color_hsv[1], board_color_hsv[2] / 2)))

        # Offsets
        self.grid_size = floor(min(width, height) / 30)
        self.board_offset_x = floor(width / 2 - self.grid_size * 9.5)
        self.board_offset_y = floor(height / 2 - self.grid_size * 9.5)


    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t

    @staticmethod
    def lerp_color(color1, color2, t):
        return tuple(int(PillowRenderer.lerp(c1, c2, t)) for c1, c2 in zip(color1, color2))

    def apply_vignetting(self, image, max_dist_ratio=1.0):
        width, height = image.size
        cx, cy = width // 2, height // 2
        max_dist = sqrt(cx**2 + cy**2) * max_dist_ratio

        vignette_color = (0, 0, 0)
        for y in range(height):
            for x in range(width):
                distance = sqrt((x - cx)**2 + (y - cy)**2)
                t = (distance / max_dist) ** 2
                image.putpixel((x, y), PillowRenderer.lerp_color(image.getpixel((x, y)), vignette_color, t))

    def apply_grain(self, image, noise_strength=0.055):
        width, height = image.size
        for y in range(height):
            for x in range(width):
                current_color = image.getpixel((x, y))

                # Chromatic noise
                noise_color = tuple(random.randint(0, 255) for _ in range(3))
                t = noise_strength * random.random() * 2
                noise_color = PillowRenderer.lerp_color(current_color, noise_color, t)

                # Grey noise
                grey_value = random.randint(0, 255)
                grey_color = (grey_value, grey_value, grey_value)
                t = noise_strength * random.random() * 4
                noise_color = PillowRenderer.lerp_color(noise_color, grey_color, t)

                # Background colored noise
                t = noise_strength * random.random()
                noise_color = PillowRenderer.lerp_color(noise_color, self.board_color, t)

                image.putpixel((x, y), noise_color)

    def save(self, position, last_move):
        # Create a blank image
        image = Image.new('RGB', (self.width, self.height), self.board_color)
        draw = ImageDraw.Draw(image)

        # Draw the grid
        for i in range(19):
            draw.line([(self.board_offset_x + self.grid_size * i, 0), (self.board_offset_x + self.grid_size * i, self.height)], fill=self.white_color, width=2)
        for i in range(19):
            draw.line([(0, self.board_offset_y + self.grid_size * i), (self.width, self.board_offset_y + self.grid_size * i)], fill=self.white_color, width=2)


        # Draw the stones
        for x, row in enumerate(position[1:]):
            for y, stone in enumerate(row[1:]):
                if stone == 2:
                    draw.ellipse([(self.board_offset_x + x * self.grid_size - self.grid_size / 2, self.board_offset_y + y * self.grid_size - self.grid_size / 2),
                                (self.board_offset_x + x * self.grid_size + self.grid_size / 2, self.board_offset_y + y * self.grid_size + self.grid_size / 2)],
                                fill=self.white_color)
                elif stone == 1:
                    draw.ellipse([(self.board_offset_x + x * self.grid_size - self.grid_size / 2, self.board_offset_y + y * self.grid_size - self.grid_size / 2),
                                (self.board_offset_x + x * self.grid_size + self.grid_size / 2, self.board_offset_y + y * self.grid_size + self.grid_size / 2)],
                                fill=self.black_color)

        # Highlight the most recent move
        highlight_color = self.white_color if position[last_move[1] + 1][last_move[0] + 1] == 1 else self.black_color
        draw.line([(self.board_offset_x + last_move[1] * self.grid_size - self.grid_size / 5,
                    self.board_offset_y + last_move[0] * self.grid_size - self.grid_size / 5),
                (self.board_offset_x + last_move[1] * self.grid_size + self.grid_size / 5,
                    self.board_offset_y + last_move[0] * self.grid_size + self.grid_size / 5)],
                fill=highlight_color,
                width=2)
        draw.line([(self.board_offset_x + last_move[1] * self.grid_size - self.grid_size / 5,
                    self.board_offset_y + last_move[0] * self.grid_size + self.grid_size / 5),
                (self.board_offset_x + last_move[1] * self.grid_size + self.grid_size / 5,
                    self.board_offset_y + last_move[0] * self.grid_size - self.grid_size / 5)],
                fill=highlight_color,
                width=2)


        # Apply grain
        self.apply_grain(image)

        # Apply vignetting
        self.apply_vignetting(image)

        # Apply Gaussian blur filter for anti-aliasing
        image = image.filter(ImageFilter.GaussianBlur(0.5))

        # Save the image
        image.save(self.output_path)
