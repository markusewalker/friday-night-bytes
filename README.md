# Friday Night Bytes :basketball: :football: :baseball:
"__X's and O's, with no syntax woes!__"

Friday Night Bytes is one stop shop for the sports statistics enthusiast! Utilizing `sportsipy`, this project aims to provide statistics on your favorite team on a game by game basis.

_Leagues / Sports currently supported_
- National Basketball Associaton (NBA) :basketball:
- National Footbal League (NFL) :football:
- Major League Baseball :baseball:


## Table of Contents
1. [Prerequisites](#Prerequisites)
2. [Getting Started](#Getting-Started)
3. [Running Program](#Running-Program)

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
pip3 install git+https://github.com/davidjkrause/sportsipy
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
usage: main.py [-h] [--sport SPORT] [--nba-teams NBA_TEAMS] [--nfl-teams NFL_TEAMS] [--mlb-teams MLB_TEAMS]

Friday Night Bytes CLI

options:
  -h, --help            show this help message and exit
  --sport SPORT, -s SPORT
                        Favorite sport number (i.e. 1 for NBA, 2 for NFL, 3 for MLB)
  --nba-teams NBA_TEAMS
                        Comma-separated NBA team abbreviations (i.e. lal,bos,mia)
  --nfl-teams NFL_TEAMS
                        Comma-separated NFL team abbreviations (i.e. phi,kc,sf)
  --mlb-teams MLB_TEAMS
                        Comma-separated MLB team abbreviations (i.e. lad, nyy, bos)
```

## 🚧 Coming soon 🚧
- Support for Pushover app to work with Github Actions
- Checking statistics for pre-game, live game and post-game for players/teams