# pylint: disable=line-too-long
"""
Utilities file
"""
import argparse
import os
import re
from typing import Literal

import numpy as np


def parse_args() -> tuple[set[str], set[str], str]:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser("Bing \"Image of The Day\" Archive Scraper")
    parser.add_argument("-y", "--blacklist_years", nargs="?",
                        help="What year(s) do you want to NOT download.\nFormat: YYYY or YYYY,YYYY,YYYY for multiple years",
                        type=str)
    parser.add_argument("-d", "--blacklist_days", nargs="?",
                        help="What specific days to you want to NOT download.\nFormat: YYYY-DD-MM or YYYY-DD-MM,YYYY-DD-MM for multiple days",
                        type=str)
    parser.add_argument("-w", "--dir", default="wallpapers")
    args = parser.parse_args()
    years = args.blacklist_years or set()
    days = args.blacklist_days or set()
    if args.blacklist_years:
        years = set(years.split(","))
        for year in years:
            assert re.match(r"\d{4}", year), f"Invalid year format: {year}"
    if args.blacklist_days:
        days = set(days.split(","))
        for day in days:
            assert re.match(r"\d{4}-\d{2}-\d{2}", day), f"Invalid day format: {day}"

    return years, days, args.dir

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


def get_already_downloaded(wallpaper_dir: str, blacklist: list[str]) -> set[str]:
    """Get a set of all the dates that have already been downloaded"""
    downloaded = set(blacklist)
    for filename in os.listdir(wallpaper_dir):
        if filename.endswith(".png"):
            downloaded.add(filename[:-4])
    return downloaded
