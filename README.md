# Bedwars Shop Generator

## About

This is a script that will generate a picture of a Player bedwars quickshop layout using the Hypixel API. \
Output, this is for example gamerboy80 quick shop\
![gamerboy80](/output/gamerboy80.png)

## Install

Copy the .env.example file and paste your API key

```bash
cp .env.example .env
```

## Usage

Simply call it and pass the username, make sure to be in the same directory as the bedwarsshop.py file.

```bash
uv run bedwarsshop <username>
```

You can always run the help command

```bash
uv run bedwarsshop --help
```

For more customizations check out constants.py file. For adjusting colors, thicknesses or adding more icon support.
I did this project a few years ago and though I would rewrite it with cleaner code and more conventional structure \
Use this script at your own risk
