from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)

import os

PUSHOVER_USER_KEY    = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN   = os.getenv("PUSHOVER_API_TOKEN")

SUPPORTED_LEAGUES = {
    "nba": {
        "name": "Basketball (NBA)",
        "teams": [
            ("Atlanta Hawks", "ATL"),
            ("Boston Celtics", "BOS"),
            ("Brooklyn Nets", "BRK"),
            ("Charlotte Hornets", "CHO"),
            ("Chicago Bulls", "CHI"),
            ("Cleveland Cavaliers", "CLE"),
            ("Dallas Mavericks", "DAL"),
            ("Denver Nuggets", "DEN"),
            ("Detroit Pistons", "DET"),
            ("Golden State Warriors", "GSW"),
            ("Houston Rockets", "HOU"),
            ("Indiana Pacers", "IND"),
            ("Los Angeles Clippers", "LAC"),
            ("Los Angeles Lakers", "LAL"),
            ("Memphis Grizzlies", "MEM"),
            ("Miami Heat", "MIA"),
            ("Milwaukee Bucks", "MIL"),
            ("Minnesota Timberwolves", "MIN"),
            ("New Orleans Pelicans", "NOP"),
            ("New York Knicks", "NYK"),
            ("Oklahoma City Thunder", "OKC"),
            ("Orlando Magic", "ORL"),
            ("Philadelphia 76ers", "PHI"),
            ("Phoenix Suns", "PHO"),
            ("Portland Trail Blazers", "POR"),
            ("Sacramento Kings", "SAC"),
            ("San Antonio Spurs", "SAS"),
            ("Toronto Raptors", "TOR"),
            ("Utah Jazz", "UTA"),
            ("Washington Wizards", "WAS")
        ]
    },
    "nfl": {
        "name": "Football (NFL)",
        "teams": [
            ("Arizona Cardinals", "ARI"),
            ("Atlanta Falcons", "ATL"),
            ("Baltimore Ravens", "BAL"),
            ("Buffalo Bills", "BUF"),
            ("Carolina Panthers", "CAR"),
            ("Chicago Bears", "CHI"),
            ("Cincinnati Bengals", "CIN"),
            ("Cleveland Browns", "CLE"),
            ("Dallas Cowboys", "DAL"),
            ("Denver Broncos", "DEN"),
            ("Detroit Lions", "DET"),
            ("Green Bay Packers", "GB"),
            ("Houston Texans", "HOU"),
            ("Indianapolis Colts", "IND"),
            ("Jacksonville Jaguars", "JAX"),
            ("Kansas City Chiefs", "KC"),
            ("Las Vegas Raiders", "LV"),
            ("Los Angeles Chargers", "LAC"),
            ("Los Angeles Rams", "LAR"),
            ("Miami Dolphins", "MIA"),
            ("Minnesota Vikings", "MIN"),
            ("New England Patriots", "NE"),
            ("New Orleans Saints", "NO"),
            ("New York Giants", "NYG"),
            ("New York Jets", "NYJ"),
            ("Philadelphia Eagles", "PHI"),
            ("Pittsburgh Steelers", "PIT"),
            ("San Francisco 49ers", "SF"),
            ("Seattle Seahawks", "SEA"),
            ("Tampa Bay Buccaneers", "TB"),
            ("Tennessee Titans", "TEN")
        ]
    },
    "mlb": {
        "name": "Baseball (MLB)",
        "teams": [
            ("Arizona Diamondbacks", "ARI"),
            ("Atlanta Braves", "ATL"),
            ("Baltimore Orioles", "BAL"),
            ("Boston Red Sox", "BOS"),
            ("Chicago Cubs", "CHC"),
            ("Chicago White Sox", "CWS"),
            ("Cincinnati Reds", "CIN"),
            ("Cleveland Guardians", "CLE"),
            ("Colorado Rockies", "COL"),
            ("Detroit Tigers", "DET"),
            ("Houston Astros", "HOU"),
            ("Kansas City Royals", "KC"),
            ("Los Angeles Angels", "LAA"),
            ("Los Angeles Dodgers", "LAD"),
            ("Miami Marlins", "MIA"),
            ("Milwaukee Brewers", "MIL"),
            ("Minnesota Twins", "MIN"),
            ("New York Mets", "NYM"),
            ("New York Yankees", "NYY"),
            ("Oakland Athletics", "OAK"),
            ("Philadelphia Phillies", "PHI"),
            ("Pittsburgh Pirates", "PIT"),
            ("San Diego Padres", "SD"),
            ("San Francisco Giants", "SF"),
            ("Seattle Mariners", "SEA"),
            ("St. Louis Cardinals", "STL"),
            ("Tampa Bay Rays", "TB"),
            ("Texas Rangers", "TEX"),
            ("Toronto Blue Jays", "TOR"),
            ("Washington Nationals", "WSH")
        ]
    },
}