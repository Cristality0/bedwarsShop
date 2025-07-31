"""Tests for bedwarsshop.bedwarsshop module."""

from click.testing import CliRunner

from bedwarsshop.bedwarsshop import main


class TestMain:
    """Tests for main function."""

    def test_main_success_flow(self, mocker, sample_player_data):
        """Test successful execution of main function."""
        # Mock all the helper functions
        mock_load_constants = mocker.patch(
            "bedwarsshop.bedwarsshop.load_constants", return_value=True
        )
        mock_get_player_data = mocker.patch(
            "bedwarsshop.bedwarsshop.get_player_data", return_value=sample_player_data
        )
        mock_parse_player_data = mocker.patch(
            "bedwarsshop.bedwarsshop.parse_player_data",
            return_value=[["stone_sword"] * 7] * 3,
        )
        mock_create_image = mocker.patch("bedwarsshop.bedwarsshop.create_image")

        runner = CliRunner()
        result = runner.invoke(main, ["testuser"])

        assert result.exit_code == 0
        mock_load_constants.assert_called_once()
        mock_get_player_data.assert_called_once_with("testuser")
        mock_parse_player_data.assert_called_once_with(sample_player_data)
        mock_create_image.assert_called_once()

    def test_main_load_constants_failure(self, mocker):
        """Test main function when load_constants fails."""
        mock_load_constants = mocker.patch(
            "bedwarsshop.bedwarsshop.load_constants", return_value=None
        )
        mock_get_player_data = mocker.patch("bedwarsshop.bedwarsshop.get_player_data")

        runner = CliRunner()
        result = runner.invoke(main, ["testuser"])

        assert (
            result.exit_code == 0
        )  # Function returns None but doesn't exit with error code
        mock_load_constants.assert_called_once()
        mock_get_player_data.assert_not_called()

    def test_main_get_player_data_failure(self, mocker):
        """Test main function when get_player_data fails."""
        mock_load_constants = mocker.patch(
            "bedwarsshop.bedwarsshop.load_constants", return_value=True
        )
        mock_get_player_data = mocker.patch(
            "bedwarsshop.bedwarsshop.get_player_data", return_value=None
        )
        mock_parse_player_data = mocker.patch(
            "bedwarsshop.bedwarsshop.parse_player_data"
        )

        runner = CliRunner()
        result = runner.invoke(main, ["testuser"])

        assert result.exit_code == 0
        mock_load_constants.assert_called_once()
        mock_get_player_data.assert_called_once_with("testuser")
        mock_parse_player_data.assert_not_called()

    def test_main_parse_player_data_failure(self, mocker, sample_player_data):
        """Test main function when parse_player_data fails."""
        mock_load_constants = mocker.patch(
            "bedwarsshop.bedwarsshop.load_constants", return_value=True
        )
        mock_get_player_data = mocker.patch(
            "bedwarsshop.bedwarsshop.get_player_data", return_value=sample_player_data
        )
        mock_parse_player_data = mocker.patch(
            "bedwarsshop.bedwarsshop.parse_player_data", return_value=None
        )
        mock_create_image = mocker.patch("bedwarsshop.bedwarsshop.create_image")

        runner = CliRunner()
        result = runner.invoke(main, ["testuser"])

        assert result.exit_code == 0
        mock_load_constants.assert_called_once()
        mock_get_player_data.assert_called_once_with("testuser")
        mock_parse_player_data.assert_called_once_with(sample_player_data)
        mock_create_image.assert_not_called()

    def test_main_with_different_player_names(self, mocker, sample_player_data):
        """Test main function with different player names."""
        # Mock all the helper functions
        mocker.patch("bedwarsshop.bedwarsshop.load_constants", return_value=True)
        mock_get_player_data = mocker.patch(
            "bedwarsshop.bedwarsshop.get_player_data", return_value=sample_player_data
        )
        mocker.patch(
            "bedwarsshop.bedwarsshop.parse_player_data",
            return_value=[["stone_sword"] * 7] * 3,
        )
        mocker.patch("bedwarsshop.bedwarsshop.create_image")

        runner = CliRunner()

        # Test with different player names
        test_names = ["gamerboy80", "Technoblade", "Dream", "user_with_underscores"]

        for name in test_names:
            result = runner.invoke(main, [name])
            assert result.exit_code == 0
            mock_get_player_data.assert_called_with(name)

    def test_main_help_command(self):
        """Test that help command works."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "generates a bedwars shop favorites image" in result.output
        assert "player_name" in result.output

    def test_main_missing_argument(self):
        """Test main function without required player_name argument."""
        runner = CliRunner()
        result = runner.invoke(main, [])

        assert result.exit_code != 0
        assert "Missing argument" in result.output or "Usage:" in result.output
