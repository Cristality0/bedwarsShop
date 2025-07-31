"""Tests for bedwarsshop.helpers module."""

import json
from unittest.mock import MagicMock, mock_open

from bedwarsshop.helpers import (
    create_image,
    get_player_data,
    load_constants,
    parse_player_data,
)


class TestLoadConstants:
    """Tests for load_constants function."""

    def test_load_constants_success(self, mock_api_key, mock_cache_and_output_dirs):
        """Test successful loading of constants."""
        result = load_constants()
        assert result is True

        # Check that directories were created
        assert mock_cache_and_output_dirs["cache_dir"].exists()
        assert mock_cache_and_output_dirs["output_dir"].exists()

    def test_load_constants_no_api_key(self, monkeypatch):
        """Test load_constants when API key is not set."""
        monkeypatch.delenv("HYPIXEL_API_KEY", raising=False)
        result = load_constants()
        assert result is None

    def test_load_constants_creates_directories(self, mock_api_key, mocker):
        """Test that load_constants creates necessary directories."""
        mock_path = mocker.patch("bedwarsshop.helpers.Path")
        mock_cache_dir = MagicMock()
        mock_output_dir = MagicMock()

        mock_path.side_effect = [mock_cache_dir, mock_output_dir]

        result = load_constants()

        assert result is True
        mock_cache_dir.mkdir.assert_called_once_with(exist_ok=True)
        mock_output_dir.mkdir.assert_called_once_with(exist_ok=True)


class TestGetPlayerData:
    """Tests for get_player_data function."""

    def test_get_player_data_from_cache(self, mock_api_key, sample_player_data, mocker):
        """Test getting player data from cache."""
        # Mock os.path.exists to return True (cache exists)
        mocker.patch("os.path.exists", return_value=True)

        # Mock file opening and JSON loading
        mock_file_open = mock_open(read_data=json.dumps(sample_player_data))
        mocker.patch("builtins.open", mock_file_open)

        result = get_player_data("testuser")

        assert result == sample_player_data
        mock_file_open.assert_called_once_with("cache/testuser.json")

    def test_get_player_data_from_api_success(
        self, mock_api_key, sample_player_data, mock_requests_get, mocker
    ):
        """Test successful API call for player data."""
        # Mock cache not existing
        mocker.patch("os.path.exists", return_value=False)

        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_player_data
        mock_requests_get.return_value = mock_response

        # Mock file writing
        mock_file_open = mock_open()
        mocker.patch("builtins.open", mock_file_open)

        result = get_player_data("testuser")

        assert result == sample_player_data
        mock_requests_get.assert_called_once()
        assert "testuser" in mock_requests_get.call_args[0][0]

    def test_get_player_data_api_failure(self, mock_api_key, mock_requests_get, mocker):
        """Test API failure when getting player data."""
        # Mock cache not existing
        mocker.patch("os.path.exists", return_value=False)

        # Mock failed API response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        result = get_player_data("nonexistentuser")

        assert result is None

    def test_get_player_data_saves_to_cache(
        self, mock_api_key, sample_player_data, mock_requests_get, mocker
    ):
        """Test that API response is saved to cache."""
        # Mock cache not existing
        mocker.patch("os.path.exists", return_value=False)

        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_player_data
        mock_requests_get.return_value = mock_response

        # Mock file writing
        mock_file_open = mock_open()
        mocker.patch("builtins.open", mock_file_open)
        mock_json_dump = mocker.patch("json.dump")

        result = get_player_data("testuser")

        assert result == sample_player_data
        mock_file_open.assert_called_with("cache/testuser.json", "w")
        mock_json_dump.assert_called_once_with(sample_player_data, mock_file_open())


class TestParsePlayerData:
    """Tests for parse_player_data function."""

    def test_parse_player_data_success(self, sample_player_data):
        """Test successful parsing of player data."""
        result = parse_player_data(sample_player_data)

        assert isinstance(result, list)
        assert len(result) == 3  # 3 rows
        assert all(len(row) == 7 for row in result)  # 7 columns each

        # Check first few items
        assert result[0][0] == "stone_sword"
        assert result[0][1] == "bridge_egg"
        assert result[0][2] == "wooden_axe"

    def test_parse_player_data_failure_not_success(self, invalid_player_data):
        """Test parsing when player data indicates failure."""
        result = parse_player_data(invalid_player_data)
        assert result is None

    def test_parse_player_data_missing_bedwars_stats(self, player_data_no_bedwars):
        """Test parsing when bedwars stats are missing."""
        result = parse_player_data(player_data_no_bedwars)
        assert result is None

    def test_parse_player_data_structure(self, sample_player_data):
        """Test the structure of parsed player data."""
        result = parse_player_data(sample_player_data)

        # Should be a 3x7 grid
        assert len(result) == 3
        for row in result:
            assert len(row) == 7

        # Test that we get the expected number of items (21 total)
        flat_items = [item for row in result for item in row]
        assert len(flat_items) == 21


class TestCreateImage:
    """Tests for create_image function."""

    def test_create_image_basic_structure(self, mock_image_operations, mocker):
        """Test basic image creation structure."""
        # Mock Path operations
        mock_path = mocker.patch("bedwarsshop.helpers.Path")
        # Set up complex mock chain for Path operations
        mock_chain = mock_path.return_value.__truediv__.return_value
        mock_chain = mock_chain.__truediv__.return_value.__truediv__.return_value
        mock_chain = "mocked_icon_path"

        # Mock the __file__ attribute in the helpers module
        mocker.patch("bedwarsshop.helpers.__file__", "/fake/path/helpers.py")

        sample_data = [
            ["stone_sword", "bridge_egg", "null", "bow", "arrow", "tnt", "end_stone"],
            [
                "iron_sword",
                "iron_boots",
                "null",
                "wooden_pickaxe",
                "water_bucket",
                "ladder",
                "shears",
            ],
            [
                "wool",
                "golden_apple",
                "magic_milk",
                "ender_pearl",
                "diamond_boots",
                "fireball",
                "diamond_sword",
            ],
        ]

        create_image(sample_data, "testuser")

        # Verify Image.new was called with correct parameters
        mock_image_operations["image"].save.assert_called_once()

    def test_create_image_handles_null_items(self, mock_image_operations, mocker):
        """Test that create_image properly handles 'null' items."""
        # Mock Path operations
        mocker.patch("bedwarsshop.helpers.Path")

        sample_data = [
            ["null", "null", "null", "null", "null", "null", "null"],
            ["null", "null", "null", "null", "null", "null", "null"],
            ["null", "null", "null", "null", "null", "null", "null"],
        ]

        # Should not raise any errors
        create_image(sample_data, "testuser")

        # Image should still be created and saved
        mock_image_operations["image"].save.assert_called_once()

    def test_create_image_unknown_items(self, mock_image_operations, mocker):
        """Test create_image with items not in ICONS_DICT."""
        # Mock Path operations
        mocker.patch("bedwarsshop.helpers.Path")

        sample_data = [
            ["unknown_item", "another_unknown", "null", "null", "null", "null", "null"],
            ["null", "null", "null", "null", "null", "null", "null"],
            ["null", "null", "null", "null", "null", "null", "null"],
        ]

        # Should not raise any errors
        create_image(sample_data, "testuser")

        # Image should still be created and saved
        mock_image_operations["image"].save.assert_called_once()

        # Text should still be drawn for unknown items
        assert (
            mock_image_operations["draw"].text.call_count >= 2
        )  # At least 2 text calls

    def test_create_image_grid_drawing(self, mock_image_operations, mocker):
        """Test that create_image draws the grid properly."""
        # Mock Path operations
        mocker.patch("bedwarsshop.helpers.Path")

        sample_data = [
            ["stone_sword", "null", "null", "null", "null", "null", "null"],
            ["null", "null", "null", "null", "null", "null", "null"],
            ["null", "null", "null", "null", "null", "null", "null"],
        ]

        create_image(sample_data, "testuser")

        # Should draw grid lines (8 vertical + 4 horizontal lines)
        expected_line_calls = 8 + 4  # 8 vertical, 4 horizontal
        assert mock_image_operations["draw"].line.call_count == expected_line_calls

    def test_create_image_file_save_path(self, mock_image_operations, mocker):
        """Test that create_image saves to the correct path."""
        # Mock Path operations
        mock_path_class = mocker.patch("bedwarsshop.helpers.Path")
        mock_path_instance = MagicMock()
        mock_path_class.return_value = mock_path_instance

        sample_data = [["null"] * 7] * 3
        player_name = "testuser"

        create_image(sample_data, player_name)

        # Check that Path was called with "output"
        assert any("output" in str(call) for call in mock_path_class.call_args_list)
