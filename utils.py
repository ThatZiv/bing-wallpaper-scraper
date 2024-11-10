from typing import Literal
import numpy as np
import os

def is_bright_image(image, region: Literal['bottom_right'] | Literal['top_half'] | Literal['bottom_half'] | Literal['bottom_left'] | None) -> bool:
    """Determine if an image is overall bright or dark"""
    image_rgb = image.convert("RGB")
    width, height = image.size
    if region == 'bottom_right':
        image_rgb = image_rgb.crop((width // 3, height // 4, width, height))
    elif region == 'top_half':
        image_rgb = image_rgb.crop((0, 0, width, height // 2))
    elif region == 'bottom_half':
        image_rgb = image_rgb.crop((0, height // 2, width, height))
    elif region == 'bottom_left':
        image_rgb = image_rgb.crop((0, height // 2, width, width // 2))
    np_image = np.array(image_rgb)
    avg_color = np.mean(np_image, axis=(0, 1))  # Average across height and width
    avg_r, avg_g, avg_b = avg_color
    luminance = 0.2126 * avg_r + 0.7152 * avg_g + 0.0722 * avg_b
    return luminance > 140 # arbitrary threshold

def get_already_downloaded(dir: str, blacklist: list[str]) -> set[str]:
    """Get a set of all the dates that have already been downloaded"""
    downloaded = set(blacklist)
    for filename in os.listdir(dir):
        if filename.endswith(".png"):
            downloaded.add(filename[:-4])
    return downloaded