import json
import logging
import os
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

from . import constants as c


def load_constants():
    global API_KEY
    # check if API key is set
    API_KEY = os.getenv("HYPIXEL_API_KEY")
    if not API_KEY:
        logging.error("API key not set")
        return None
    # Create cache directory in current working directory
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)
    # Create output directory in current working directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    return True


def get_player_data(player_name: str):
    """
    Retrieves player data from the Hypixel API.

    Args:
        player_name (str): The name of the player.

    Returns:
        dict: The player data as a dictionary, or None if the data retrieval
        fails.
    """
    # check if player is in cache
    if os.path.exists(f"cache/{player_name}.json"):
        logging.info(f"Player data found in cache: {player_name}")
        with open(f"cache/{player_name}.json") as f:
            data = json.load(f)
            return data
    url = f"https://api.hypixel.net/v2/player?key={API_KEY}&name={player_name}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open(f"cache/{player_name}.json", "w") as f:
            json.dump(data, f)
        return data
    else:
        logging.error(
            f"Failed to retrieve player data, status code: {response.status_code}"
        )
        return None


def parse_player_data(player_data):
    """
    Parses the player data and returns a 2D array representing the layers of
    the player's Bedwars favorites.

    Args:
        player_data (dict): The player data to be parsed.

    Returns:
        list: A 2D array representing the layers of the player's Bedwars
        favorites.

    Raises:
        KeyError: If the player data does not contain the required keys.

    """
    if not player_data["success"]:
        logging.error(
            f"Failed to retrieve player data, success={player_data['success']}"
        )
        return None
    try:
        player_data = player_data["player"]["stats"]["Bedwars"]["favourites_2"]
    except (TypeError, KeyError):
        logging.error("Failed to parse player data")
        return None
    # parse string data array
    player_data = player_data.split(",")
    # split into 2d array 7x3
    layer_data = [player_data[0:7], player_data[7:14], player_data[14:21]]
    return layer_data


def create_image(player_data, player_name):
    """
    Create an image based on the player data.

    Args:
        player_data (list): A 2D list containing the player data.

    Returns:
        None
    """
    image = Image.new(mode="RGBA", size=(7 * 320, 3 * 320), color=c.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    fnt = ImageFont.truetype("arial.ttf", c.FONT_SIZE)
    for y, row in enumerate(player_data):
        for x, item in enumerate(row):
            if item == "null":
                continue
            # check if item is in icons dict
            if item in c.ICONS_DICT:
                # Get the package directory and construct icon path
                package_dir = Path(__file__).parent
                icon_path = package_dir / "assets" / "icons" / c.ICONS_DICT[item]
                icon = Image.open(icon_path)
                icon = icon.convert("RGBA")
                icon = icon.resize((320, 320))
                image.paste(icon, (x * 320, y * 320))
            # white name text
            draw.text(
                (x * 320 + 10, y * 320 + 10),
                item.replace("_", " "),
                fill=c.TEXT_COLOR,
                font=fnt,
            )
    # draw grid
    for x in range(0, 7):
        draw.line((x * 320, 0, x * 320, 3 * 320), fill=c.LINE_COLOR, width=c.LINE_WIDTH)
    draw.line(
        (7 * 320 - c.LINE_WIDTH, 0, 7 * 320 - c.LINE_WIDTH, 3 * 320),
        fill=c.LINE_COLOR,
        width=c.LINE_WIDTH,
    )
    for y in range(0, 3):
        draw.line((0, y * 320, 7 * 320, y * 320), fill=c.LINE_COLOR, width=c.LINE_WIDTH)
    draw.line(
        (0, 3 * 320 - c.LINE_WIDTH, 7 * 320, 3 * 320 - c.LINE_WIDTH),
        fill=c.LINE_COLOR,
        width=c.LINE_WIDTH,
    )
    output_path = Path("output") / f"{player_name}.png"
    image.save(output_path)
    logging.info(f"Image saved to: {output_path.absolute()}")
    if c.SHOW_IMAGE:
        image.show()
