# Bing "Image of The Day" Scraper

A script to mass-download the contents of https://bing.gifposter.com/ (Bing's image of the day) site. I use these as my desktop wallpapers

## Usage

### Use public Docker image

```sh
docker run --rm -v "$PWD/wallpapers":/app/wallpapers thatziv/bing-wallpaper-scraper:latest
```

### Build it yourself w/ Docker

```sh
# clone repo
git clone https://github.com/thatziv/bing-wallpaper-scraper

# build docker image
docker build -t bing-wallpaper-scraper

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
python main.py ~/wallpapers
```

You should see them show up in `./wallpapers`

## Samples

![img1](wallpapers/2023-12-03.png)
[Source](https://bing.gifposter.com/wallpaper-2724-vermilioncliffs.html)
![img2](wallpapers/2024-11-06.png)
[Source](https://bing.gifposter.com/uk/column-915-shi-shi-beach-olympic-national-park-washington-united-states.html)
