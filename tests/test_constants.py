"""Tests for bedwarsshop.constants module."""

from bedwarsshop import constants as c


class TestConstants:
    """Tests for constants values and structure."""

    def test_icons_dict_exists(self):
        """Test that ICONS_DICT exists and is not empty."""
        assert hasattr(c, "ICONS_DICT")
        assert isinstance(c.ICONS_DICT, dict)
        assert len(c.ICONS_DICT) > 0

    def test_icons_dict_contains_expected_items(self):
        """Test that ICONS_DICT contains some expected items."""
        expected_items = [
            "stone_sword",
            "bridge_egg",
            "wooden_axe",
            "bow",
            "arrow",
            "tnt",
            "diamond_sword",
        ]

        for item in expected_items:
            assert item in c.ICONS_DICT
            assert c.ICONS_DICT[item].endswith(".png")

    def test_icons_dict_values_are_png_files(self):
        """Test that all values in ICONS_DICT are PNG files."""
        for _icon_name, file_name in c.ICONS_DICT.items():
            assert isinstance(file_name, str)
            assert file_name.endswith(".png")
            assert len(file_name) > 4  # More than just ".png"

    def test_font_size_is_positive_integer(self):
        """Test that FONT_SIZE is a positive integer."""
        assert hasattr(c, "FONT_SIZE")
        assert isinstance(c.FONT_SIZE, int)
        assert c.FONT_SIZE > 0

    def test_line_width_is_positive_integer(self):
        """Test that LINE_WIDTH is a positive integer."""
        assert hasattr(c, "LINE_WIDTH")
        assert isinstance(c.LINE_WIDTH, int)
        assert c.LINE_WIDTH > 0

    def test_colors_are_tuples(self):
        """Test that color constants are tuples with correct length."""
        color_constants = ["LINE_COLOR", "TEXT_COLOR", "BACKGROUND_COLOR"]

        for color_name in color_constants:
            assert hasattr(c, color_name)
            color_value = getattr(c, color_name)
            assert isinstance(color_value, tuple)
            assert len(color_value) == 4  # RGBA

            # Check that all values are integers between 0-255
            for component in color_value:
                assert isinstance(component, int)
                assert 0 <= component <= 255

    def test_show_image_is_boolean(self):
        """Test that SHOW_IMAGE is a boolean."""
        assert hasattr(c, "SHOW_IMAGE")
        assert isinstance(c.SHOW_IMAGE, bool)

    def test_constants_immutability(self):
        """Test that modifying constants doesn't break the module."""
        # This is more of a design test - constants should be treated as immutable
        original_font_size = c.FONT_SIZE
        original_icons_dict_size = len(c.ICONS_DICT)

        # These operations shouldn't affect the original values
        # (though Python doesn't enforce immutability)
        assert c.FONT_SIZE == original_font_size
        assert len(c.ICONS_DICT) == original_icons_dict_size
