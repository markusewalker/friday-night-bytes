# Friday Night Bytes :basketball: :football: :baseball:
"__X's and O's, with no syntax woes!__"

Friday Night Bytes is a **proof of concept** sports game checker that demonstrates automated data collection from sports websites. Utilizing `sportsipy`, this project showcases how to build a game-checking application with robust error handling and timezone management.

**⚠️ CI/CD Limitations**: Sports data providers (like sports-reference.com) actively block automated requests from GitHub Actions and other CI environments. This is expected behavior and demonstrates real-world challenges in web scraping.

**✅ Local Usage**: The application works locally, just not with Github Actions.

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

## Getting Started
Once you have followed the prerequisites and installed all the needed dependencies, run the following commands:

```
python3 -m venv env
source env/bin/activate
pip3 install -r required_libraries.txt
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
- Checking statistics for players/teams
- GUI support