from helpers import load_constants, get_player_data, parse_player_data
from helpers import create_image
import logging
import click
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


@click.command()
@click.argument("player_name", type=str)
def main(player_name):
    """
    generates a bedwars shop favorites image for a player.
    To use this script, you need to have a Hypixel API key.
    Usage: "python run.py <player_name>"

    Args:
        player_name (str): Username of the player.

    """
    if not load_constants():
        logging.error("Failed to load constants, exiting...")
        return
    player_data = get_player_data(player_name)
    if not player_data:
        logging.error("Failed to retrieve player data, exiting...")
        return
    player_data = parse_player_data(player_data)
    if not player_data:
        logging.error("Failed to parse player data, exiting...")
        return
    print(player_data)
    create_image(player_data, player_name)


if __name__ == "__main__":
    main()
