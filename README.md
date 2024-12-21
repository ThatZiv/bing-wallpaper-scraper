# Bing "Image of The Day" Scraper

A script to mass-download the contents of https://bing.gifposter.com/ (Bing's image of the day) site. I use these as my desktop wallpapers

## Usage

```
usage: Bing "Image of The Day" Archive Scraper [-h] [-y [BLACKLIST_YEARS]] [-d [BLACKLIST_DAYS]] [-w DIR]

options:
  -h, --help            show this help message and exit
  -y [BLACKLIST_YEARS], --blacklist_years [BLACKLIST_YEARS]
                        What year(s) do you want to NOT download. Format: YYYY or YYYY,YYYY,YYYY for multiple years
  -d [BLACKLIST_DAYS], --blacklist_days [BLACKLIST_DAYS]
                        What specific days to you want to NOT download. Format: YYYY-DD-MM or YYYY-DD-MM,YYYY-DD-MM for multiple days
  -w DIR, --dir DIR

example:
    - Skip years 2018,2019,2020: -y "2018,2019,2020"
    - Skip days 2024-08-02: -d "2024-08-02"
```

### Use public Docker image

```sh
docker run --rm -v "$PWD/wallpapers":/app/wallpapers ghcr.io/thatziv/bing-wallpaper-scraper:latest
```

### Build it yourself w/ Docker

```sh
# clone repo
git clone https://github.com/thatziv/bing-wallpaper-scraper

# build docker image
docker build -t bing-wallpaper-scraper .

# run it
docker run --rm -v "$PWD/wallpapers":/app/wallpapers bing-wallpaper-scraper
```

### Build it yourself w/ Python

```sh
# clone repo
git clone https://github.com/thatziv/bing-wallpaper-scraper

# Install requirements
python -m pip install -r requirements.txt

# Run script (argument is optional)
python main.py --dir ~/wallpapers
```

You should see them show up in `./wallpapers`

## Samples

![img1](wallpapers/2023-12-03.png)
[Source](https://bing.gifposter.com/wallpaper-2724-vermilioncliffs.html)
![img2](wallpapers/2024-11-06.png)
[Source](https://bing.gifposter.com/uk/column-915-shi-shi-beach-olympic-national-park-washington-united-states.html)
