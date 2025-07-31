# Bedwars Shop Generator

[![Tests](https://github.com/YOUR_USERNAME/bedwarsShop/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/bedwarsShop/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/bedwarsShop/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/bedwarsShop)

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

## Development

### Setup

1. Clone the repository
2. Install uv if you haven't already: `pip install uv`
3. Install dependencies: `uv sync --dev`
4. Copy the .env.example file and add your API key: `cp .env.example .env`

### Testing

This project uses pytest for testing. To run the tests:

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/bedwarsshop --cov-report=html

# Run specific test file
uv run pytest tests/test_helpers.py

# Run tests with verbose output
uv run pytest -v
```

### Test Structure

- `tests/test_helpers.py` - Tests for helper functions (API calls, data parsing, image creation)
- `tests/test_bedwarsshop.py` - Integration tests for the main CLI function
- `tests/test_constants.py` - Tests for constants and configuration
- `tests/conftest.py` - Shared fixtures and test configuration

### Code Quality

The project uses ruff for linting and formatting:

```bash
# Check code style
uv run ruff check src/ tests/

# Format code
uv run ruff format src/ tests/
```

### Continuous Integration

Tests are automatically run on every push and pull request using GitHub Actions. The CI pipeline:

- Tests on Python 3.11, 3.12, and 3.13
- Runs linting and formatting checks
- Generates coverage reports
- Uploads coverage to Codecov
