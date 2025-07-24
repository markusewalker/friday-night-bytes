from datetime import datetime, date, timedelta
from sportsipy.nba.schedule import Schedule as NBASchedule
from sportsipy.nfl.schedule import Schedule as NFLSchedule
from sportsipy.mlb.schedule import Schedule as MLBSchedule
from constants import SUPPORTED_LEAGUES
import time
import requests
import pytz
import ssl
import urllib3

def get_current_date():
    """Get the current date using Eastern timezone for consistency."""
    eastern_tz = pytz.timezone('US/Eastern')
    now_eastern = datetime.now(eastern_tz)
    current_date = now_eastern.date()
    
    return current_date


def get_team_name_from_abbreviation(abbreviation, league):
    """Get the full team name from abbreviation for a specific league."""
    if league not in SUPPORTED_LEAGUES:
        return None
        
    teams = SUPPORTED_LEAGUES[league]["teams"]
    for name, abbr in teams:
        if abbr.lower() == abbreviation.lower():
            return name

    return None


def get_schedule_for_league(team_abbr, league):
    """Get schedule for a team based on the league."""
    if league == "nba":
        return NBASchedule(team_abbr.upper())
    elif league == "nfl":
        return NFLSchedule(team_abbr.upper())
    elif league == "mlb":
        return MLBSchedule(team_abbr.upper())
    else:
        raise ValueError(f"Unsupported league: {league}")


def get_date_description(target_date):
    """
    Get a readable description for the given date.
    
    Args:
        target_date (date): The date to describe
    
    Returns:
        str: Human-readable description ('today', 'tomorrow', or formatted date)
    """
    today = get_current_date()
    tomorrow = today + timedelta(days=1)
    
    if target_date == today:
        return "today"
    elif target_date == tomorrow:
        return "tomorrow"
    else:
        return target_date.strftime('%B %d, %Y')


def check_games(favorite_teams, league, target_date):
    """
    Check if any of the selected favorite teams have games scheduled for a specific date.

    Args:
        favorite_teams (list): List of team abbreviations (e.g., ['lal', 'bos'])
        league (str): The league to check (e.g., 'nba', 'nfl', 'mlb') - REQUIRED
        target_date (date): The date to check for games
    
    Returns:
        list: List of dictionaries containing game information for the target date
    """
    games_found = []
    
    if not favorite_teams or league not in SUPPORTED_LEAGUES:
        return games_found
    
    league_name = SUPPORTED_LEAGUES[league]["name"]
    date_description = get_date_description(target_date)
    print(f"\n🔍 Searching {league_name} games for {date_description}...")
    print("─" * 90)
    
    for i, team_abbr in enumerate(favorite_teams):
        team_name = get_team_name_from_abbreviation(team_abbr, league)
        if not team_name:
            print(f"   ⚠️  Unknown team: {team_abbr}")
            continue
            
        print(f"   📅 {team_name}...", end="")
        print(" " * (40 - len(team_name)), end="")
        
        try:
            # Put a sleep between requests to avoid rate limiting
            if i > 0:
                time.sleep(5)
            schedule = get_schedule_for_league(team_abbr, league)
            
            team_has_game = False
            for game in schedule:
                try:
                    game_date = parse_game_date(game.date, league)
                    if not game_date:
                        continue
                except (ValueError, AttributeError):
                    continue
                
                if game_date == target_date:
                    is_home = game.location == 'Home' if hasattr(game, 'location') else None
                    opponent = game.opponent_abbr if hasattr(game, 'opponent_abbr') else 'Unknown'
                    opponent_name = get_team_name_from_abbreviation(opponent, league)
                    
                    game_info = {
                        'league': league,
                        'league_name': league_name,
                        'team': team_name,
                        'team_abbr': team_abbr.upper(),
                        'opponent': opponent_name or opponent,
                        'opponent_abbr': opponent,
                        'is_home': is_home,
                        'date': game_date.strftime('%Y-%m-%d')
                    }
                    
                    games_found.append(game_info)
                    print(" ✅ Game Found!")
                    team_has_game = True
                    break
            
            if not team_has_game:
                print(" ❌ No game")
                    
        except requests.exceptions.HTTPError as e:
            if "429" in str(e):
                print(" ⚠️ Rate limit")
                continue
            elif "403" in str(e):
                print(" 🚫 Blocked")
            else:
                print(f" ❌ HTTP error: {str(e)}")
        except requests.exceptions.RequestException as e:
            print(f" ❌ Network error: {str(e)}")
        except Exception as e:
            if "403" in str(e) and "Forbidden" in str(e):
                print(" 🚫 Blocked (403)")
            else:
                print(f" ❌ Error: {str(e)}")
            continue
    
    return games_found


def check_games_today(favorite_teams, league):
    """
    Check if any of the selected favorite teams have games scheduled for today.

    Args:
        favorite_teams (list): List of team abbreviations (e.g., ['lal', 'bos'])
        league (str): The league to check (e.g., 'nba', 'nfl', 'mlb') - REQUIRED
    
    Returns:
        list: List of dictionaries containing game information for today
    """
    return check_games(favorite_teams, league, get_current_date())


def check_games_tomorrow(favorite_teams, league):
    """
    Check if any of the selected favorite teams have games scheduled for tomorrow.

    Args:
        favorite_teams (list): List of team abbreviations (e.g., ['lal', 'bos'])
        league (str): The league to check (e.g., 'nba', 'nfl', 'mlb') - REQUIRED
    
    Returns:
        list: List of dictionaries containing game information for tomorrow
    """
    tomorrow = get_current_date() + timedelta(days=1)
    return check_games(favorite_teams, league, tomorrow)


def display_games(games_list, target_date):
    """
    Display information about games scheduled for a specific date.
    
    Args:
        games_list (list): List of game dictionaries
        target_date (date): The date for which games are being displayed
    """
    if not games_list:
        date_description = get_date_description(target_date)
        print(f"\n📅 No games scheduled {date_description} for your favorite teams")
        return
    
    games_by_league = {}
    for game in games_list:
        league = game['league']
        if league not in games_by_league:
            games_by_league[league] = []
        games_by_league[league].append(game)
    
    date_description = get_date_description(target_date)
    print(f"\n🏆 Games {date_description.title()} • {target_date.strftime('%B %d, %Y (%A)')}")
    
    for league, games in games_by_league.items():
        print("─" * 90)
        print(f"{'Team':<35} {'Matchup':<45} {'Venue'}")
        print("─" * 90)
        
        for game in games:
            team = game['team']
            if game['is_home']:
                matchup = f"{game['team']} vs {game['opponent']}"
                venue = "🏠 Home"
            else:
                matchup = f"{game['team']} @ {game['opponent']}"
                venue = "✈️  Away"
            
            print(f"{team:<35} {matchup:<45} {venue}")
        
        print()


def display_games_today(games_today):
    """
    Display information about games scheduled for today.
    
    Args:
        games_today (list): List of game dictionaries
    """
    display_games(games_today, get_current_date())

      
def display_games_tomorrow(games_tomorrow):
    """
    Display information about games scheduled for tomorrow.
    
    Args:
        games_tomorrow (list): List of game dictionaries
    """
    tomorrow = get_current_date() + timedelta(days=1)
    display_games(games_tomorrow, tomorrow)


def parse_game_date(date_str, league):
    """
    Parse game date string based on the league's specific format.
    
    Args:
        date_str (str): The date string from the game
        league (str): The league ('nba', 'nfl', 'mlb')
    
    Returns:
        date: Parsed date object or None if parsing fails
    """
    if not date_str:
        return None
    
    current_year = get_current_date().year
    
    date_pattern = {
        'nba': '%a, %b %d, %Y',
        'mlb': '%A, %b %d',
        'nfl': '%a, %b %d, %Y',
    }

    pattern = date_pattern.get(league, '%Y-%m-%d') 

    try:
        parsed_date = datetime.strptime(date_str, pattern).date()
        
        if league == 'mlb' and parsed_date.year == 1900:
            parsed_date = parsed_date.replace(year=current_year)
        
        return parsed_date
    except (ValueError, AttributeError):
        fallback_patterns = [
            '%Y-%m-%d',
            '%A, %b %d, %Y',
            '%a, %b %d, %Y',
            '%A, %b %d',
            '%B %d, %Y',
            '%m/%d/%Y',
        ]
        
        for fallback in fallback_patterns:
            try:
                parsed_date = datetime.strptime(date_str, fallback).date()
                if parsed_date.year == 1900:
                    parsed_date = parsed_date.replace(year=current_year)
                return parsed_date
            except (ValueError, AttributeError):
                continue
        
        return None


def game_checker(preferences):
    """
    Function to check if the selected teams are playing today and tomorrow, and display the games.
    
    Args:
        preferences (dict): User preferences containing favorite teams and leagues
    """
    if not preferences:
        return
    
    all_games_today = []
    all_games_tomorrow = []
    
    for league_key in SUPPORTED_LEAGUES.keys():
        team_key = f"{league_key}_team"

        if team_key in preferences and preferences[team_key]:
            favorite_teams = preferences[team_key]
            games_today = check_games_today(favorite_teams, league_key)
            games_tomorrow = check_games_tomorrow(favorite_teams, league_key)
            all_games_today.extend(games_today)
            all_games_tomorrow.extend(games_tomorrow)
    
    display_games_today(all_games_today)
    display_games_tomorrow(all_games_tomorrow)