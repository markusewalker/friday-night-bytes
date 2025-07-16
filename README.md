# Friday Night Bytes :basketball: :football: :soccer: :baseball:
"__X's and O's, with no syntax woes!__"

Friday Night Bytes is one stop shop for the sports statistics enthusiast! Utilizing `sportsipy`, this project aims to provide statistics on your favorite team on a game by game basis.

_Leagues / Sports currently supported_
- National Basketball Associaton (NBA) :basketball:


## Table of Contents
1. [Prerequisites](#Prerequisites)
2. [Getting Started](#Getting-Started)
3. [Running Program](#Running-Program)
4. [Testing](#Testing)

## Prerequisites
In order to properly run this, you will need the following installed on your client machine:

- `python3`
- `pip` || `pip3`
- `venv`
- Pushover app installed on your device
- `ntfy` installed on Pushover

## Getting Started
Once you have followed the prerequisites and installed all the needed dependencies, run the following commands:

```
python3 -m venv env
source env/bin/activate
pip3 install -r required_libraries.txt
pip install git+https://github.com/davidjkrause/sportsipy@
```

## Running Program
To run the program, you can do so interactively or via the command line. See both options below:

_Interactively_
```
python3 main.py
```

_Command line_
```
$ python3 main.py -h
usage: main.py [-h] [--sport SPORT] [--nba-teams NBA_TEAMS]

Friday Night Bytes CLI

options:
  -h, --help            show this help message and exit
  --sport SPORT, -s SPORT
                        Favorite sport number (e.g., 1 for NBA)
  --nba-teams NBA_TEAMS
                        Comma-separated NBA team abbreviations (e.g., lal,bos,mia)
```


## Testing
`pytest` has been used to properly test this program in completeness. You can use the following command to test as an example:

```
$ pytest -m unit -s -v
==================================================================================== test session starts =====================================================================================
platform linux -- Python 3.12.3, pytest-8.4.1, pluggy-1.6.0 -- /path/to/github/friday-night-bytes/env/bin/python3
cachedir: .pytest_cache
rootdir: /path/to/github/friday-night-bytes
configfile: pyproject.toml
testpaths: tests
collected 12 items                                                                                                                                                                           

tests/test_game_checker.py::test_game_display_with_game ==================================================

Games today (July 15, 2025):
--------------------------------------------------

Basketball (NBA):
🏠 Los Angeles Lakers vs Boston Celtics
   Time: 8:00 PM EST

✈️  Miami Heat @ Golden State Warriors
   Time: 10:30 PM EST

PASSED
tests/test_game_checker.py::test_game_display_no_games ==================================================

That sucks! No games are scheduled today for your favorite teams.
PASSED
tests/test_main.py::test_get_preferences_valid_nba_team PASSED
tests/test_main.py::test_get_preferences_multiple_nba_teams PASSED
tests/test_main.py::test_get_preferences_invalid_nba_team PASSED
tests/test_main.py::test_get_preferences_one_invalid_nba_team PASSED
tests/test_main.py::test_get_preferences_no_args PASSED
tests/test_main.py::test_main_cli_short_args PASSED
tests/test_main.py::test_main_cli_valid_team PASSED
tests/test_main.py::test_main_cli_invalid_team PASSED
tests/test_main.py::test_main_cli_no_args PASSED
tests/test_main.py::test_main_cli_one_invalid_team PASSED

===================================================================================== 12 passed in 1.86s =====================================================================================
```

## 🚧 Coming soon 🚧
- Support for Pushover app to work with Github Actions
- Checking statistics for pre-game, live game and post-game for players/teams
- Support for National Football League (NFL) :football:
- Support for Major League Baseball (MLB) :baseball:
- Support for Major League Soccer (MLS) :soccer: