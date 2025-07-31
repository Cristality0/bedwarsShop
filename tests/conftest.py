"""Pytest configuration and shared fixtures for bedwarsshop tests."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PIL import Image


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_api_key(monkeypatch):
    """Mock the HYPIXEL_API_KEY environment variable."""
    test_api_key = "test-api-key-12345"
    monkeypatch.setenv("HYPIXEL_API_KEY", test_api_key)
    return test_api_key


@pytest.fixture
def sample_player_data():
    """Sample player data for testing."""
    return {
        "success": True,
        "player": {
            "stats": {
                "Bedwars": {
                    "favourites_2": (
                        "stone_sword,bridge_egg,wooden_axe,bow,arrow,"
                        "invisibility_potion_(30_seconds),tnt,end_stone,iron_sword,"
                        "iron_boots,chainmail_boots,wooden_pickaxe,"
                        "jump_v_potion_(45_seconds),water_bucket,oak_wood_planks,"
                        "ladder,shears,wool,golden_apple,speed_ii_potion_(45_seconds),"
                        "magic_milk"
                    )
                }
            }
        },
    }


@pytest.fixture
def invalid_player_data():
    """Invalid player data for testing error cases."""
    return {"success": False, "cause": "Invalid API key"}


@pytest.fixture
def player_data_no_bedwars():
    """Player data without bedwars stats."""
    return {"success": True, "player": {"stats": {}}}


@pytest.fixture
def mock_requests_get(mocker):
    """Mock requests.get function."""
    return mocker.patch("bedwarsshop.helpers.requests.get")


@pytest.fixture
def mock_image_operations(mocker):
    """Mock PIL Image operations."""
    mock_image = MagicMock()
    mock_draw = MagicMock()
    mock_font = MagicMock()

    mocker.patch("bedwarsshop.helpers.Image.new", return_value=mock_image)
    mocker.patch("bedwarsshop.helpers.ImageDraw.Draw", return_value=mock_draw)
    mocker.patch("bedwarsshop.helpers.ImageFont.truetype", return_value=mock_font)
    mocker.patch("bedwarsshop.helpers.Image.open", return_value=mock_image)

    return {"image": mock_image, "draw": mock_draw, "font": mock_font}


@pytest.fixture
def mock_cache_and_output_dirs(mocker, temp_dir):
    """Mock cache and output directory creation."""
    cache_dir = temp_dir / "cache"
    output_dir = temp_dir / "output"
    cache_dir.mkdir()
    output_dir.mkdir()

    # Mock Path to return our temporary directories
    mocker.patch("bedwarsshop.helpers.Path", side_effect=lambda x: temp_dir / x)

    return {"cache_dir": cache_dir, "output_dir": output_dir, "temp_dir": temp_dir}


@pytest.fixture
def sample_icon_file(temp_dir):
    """Create a sample icon file for testing."""
    icons_dir = temp_dir / "src" / "bedwarsshop" / "assets" / "icons"
    icons_dir.mkdir(parents=True)

    # Create a simple test image
    test_image = Image.new("RGBA", (64, 64), (255, 0, 0, 255))
    icon_path = icons_dir / "stone_sword.png"
    test_image.save(icon_path)

    return icon_path
