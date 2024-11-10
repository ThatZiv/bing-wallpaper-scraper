import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from io import BytesIO
import os
import sys
from utils import is_bright_image, get_already_downloaded

WALLPAPER_DEFAULT_DIR = "wallpapers"
BLACKLISTED = ["2020-07-17"]
# get from environment variable, or command line argument, or new folder called wallpapers
wallpaper_dir = os.environ.get("WALLPAPER_DIR", sys.argv[1] if len(sys.argv) > 1 else WALLPAPER_DEFAULT_DIR)

primary_font = ImageFont.truetype("IBMPlexSans-Regular.ttf", 35)
secondary_font = ImageFont.truetype("IBMPlexSans-Regular.ttf", 20)

def main() -> None:
    """Scrape the Bing wallpaper archive and download respective images"""
    base_url = "https://bing.gifposter.com"
    archive_url = f"https://bing.gifposter.com/archive/{datetime.now().strftime('%Y%m')}.html" # starting point
    os.makedirs(wallpaper_dir, exist_ok=True)
    res = requests.get(archive_url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    start = datetime.now()
    print("Checking for already downloaded images...")
    done = get_already_downloaded(dir=wallpaper_dir, blacklist=BLACKLISTED)
    print(f"Found {len(done)} images.")
    for a in soup.find_all("a"):
        # TODO: this high level scraping isn't really necessary
        month_ref = a.get("href")
        if month_ref.startswith("/archive/") and month_ref.endswith(".html"):
            month_page = base_url + month_ref
            res = requests.get(month_page, timeout=15)
            _soup = BeautifulSoup(res.text, "html.parser")
            for wallpaper_page_anchor in _soup.find_all("a"):
                wallpaper_page = wallpaper_page_anchor.get("href")
                if wallpaper_page.startswith("/wallpaper-") and wallpaper_page.endswith(".html"):
                    metadata = wallpaper_page_anchor.find("h3")
                    # time is in format YYYY-MM-DD
                    date = metadata.find("time").text
                    if date in done:
                        print(f"Skipping {date} (already downloaded)")
                        continue
                    # format data as Month Day, Year
                    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")
                    location = metadata.find("span").text
                    img_url = wallpaper_page_anchor.find('img').get('src')[:-3]
                    # download image
                    img_res = requests.get(img_url, timeout=10)
                    img = Image.open(BytesIO(img_res.content))
                    draw = ImageDraw.Draw(img)

                    color = (0, 0, 0, 180) if is_bright_image(img, region='bottom_right') else (255, 255, 255, 150)
                    draw.text((img.width - 35, img.height - 100), f"{location}", font=primary_font, fill=color, anchor="rt")
                    draw.text((img.width - 35, img.height - 125), f"{formatted_date}", font=secondary_font, fill=color, anchor="rt")
                    img.save(f"{wallpaper_dir}/{date}.png")
                    print(f"Saved {date}.png")
                    done.add(date)

    print(f"Finished in: {(datetime.now() - start).total_seconds()//60}m")

if __name__ == "__main__":
    main()