from datetime import datetime, date, timedelta
from constants import SUPPORTED_LEAGUES
import time
import requests
import pytz
import ssl
import json
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def get_schedule_from_espn(league, team_abbr):
    """Get schedule from ESPN API for a specific team in any league"""
    sport_paths = {
        'nfl': 'football/nfl',
        'nba': 'basketball/nba', 
        'mlb': 'baseball/mlb'
    }
    
    sport_path = sport_paths.get(league)
    if not sport_path:
        print(f"Unsupported league: {league}")
        return []
    
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/{sport_path}/teams/{team_abbr}/schedule"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        games = []
        events = data.get('events', [])
        
        for event in events:
            competitors = event.get('competitions', [{}])[0].get('competitors', [])
            for competitor in competitors:
                team_data = competitor.get('team', {})

                if team_data.get('abbreviation', '').upper() == team_abbr.upper():
                    opponent = None
                    for comp in competitors:
                        if comp != competitor:
                            opponent = comp.get('team', {}).get('abbreviation', 'Unknown')
                            break
                    
                    game_info = {
                        'date': event.get('date', ''),
                        'opponent_abbr': opponent,
                        'location': 'Home' if competitor.get('homeAway') == 'home' else 'Away'
                    }

                    games.append(game_info)
                    break
        
        return games
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {league.upper()} schedule for {team_abbr}: {e}")
        return []


def get_schedule_for_league(league, team_abbr):
    """Get schedule data for a team in the specified league"""
    return get_schedule_from_espn(league, team_abbr)


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
                time.sleep(0.5)  # Reduced sleep time since ESPN is more reliable
            schedule = get_schedule_for_league(league, team_abbr)
            
            team_has_game = False
            
            for game in schedule:
                try:
                    game_date_str = game.get('date', '')
                    if game_date_str:
                        game_date = datetime.fromisoformat(game_date_str.replace('Z', '+00:00')).date()
                    else:
                        continue
                except (ValueError, AttributeError):
                    continue
                
                if game_date == target_date:
                    is_home = game.get('location') == 'Home'
                    opponent = game.get('opponent_abbr', 'Unknown')
                    opponent_name = get_team_name_from_abbreviation(opponent, league)
                    
                    game_info = {
                        'league': league,
                        'league_name': league_name,
                        'team': team_name,
                        'team_abbr': team_abbr.upper(),
                        'opponent': opponent_name or opponent,
                        'opponent_abbr': opponent,
                        'is_home': is_home,
                        'date': game_date.strftime('%Y-%m-%d'),
                        'datetime': game.get('date', '')
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


def check_games_this_week(favorite_teams, league):
    """
    Check if any of the selected favorite teams have games scheduled for this week.

    Args:
        favorite_teams (list): List of team abbreviations (e.g., ['lal', 'bos'])
        league (str): The league to check (e.g., 'nba', 'nfl', 'mlb') - REQUIRED
    
    Returns:
        dict: Dictionary with dates as keys and lists of game information as values
    """
    weekly_games = {}
    current_date = get_current_date()
    
    for day_offset in range(7):
        target_date = current_date + timedelta(days=day_offset)
        games_for_date = check_games(favorite_teams, league, target_date)

        if games_for_date:
            weekly_games[target_date] = games_for_date
    
    return weekly_games


def display_games(games_list):
    """
    Display information about games scheduled for your favorite teams.
    
    Args:
        games_list (list): List of game dictionaries
    """
    if not games_list:
        print(f"\n📅 No games scheduled for your favorite teams")
        return
    
    games_by_league = {}
    for game in games_list:
        league = game['league']
        if league not in games_by_league:
            games_by_league[league] = []
        games_by_league[league].append(game)
    
    print(f"\nGames for your favorite teams")
    
    for league, games in games_by_league.items():
        print("─" * 90)
        print(f"{'Team':<35} {'Matchup':<45} {'Venue'}")
        print("─" * 90)
        
        for game in games:
            team = game['team']
            if game['is_home']:
                matchup = f"{game['team']} vs {game['opponent']}"
                venue = "🏠"
            else:
                matchup = f"{game['team']} @ {game['opponent']}"
                venue = "✈️ "
            
            game_datetime = game.get('datetime', '')
            if game_datetime and 'T' in game_datetime:
                try:
                    dt = datetime.fromisoformat(game_datetime.replace('Z', '+00:00'))
                    eastern = pytz.timezone('America/New_York')
                    dt_et = dt.astimezone(eastern)

                    game_date = dt_et.strftime('%m/%d/%Y')
                    game_time = dt_et.strftime('%I:%M %p EST')

                    date_time_display = f"{game_date} {game_time}"
                except Exception as e:
                    date_time_display = game_datetime
            else:
                date_time_display = 'TBD'
                
            print(f"{team:<35} {matchup:<45} {venue} {date_time_display}")
        
        print()


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
    

def build_games_summary(games, label):
    """
    Helper to build a summary string for a list of games.
    """
    lines = [label]

    if games:
        for game in games:
            venue = "Home"

            if game.get('is_home'):
                venue = "🏠"
            else:
                venue = "✈️"

            lines.append(f"🏆{game['team']} vs {game['opponent']} {venue}")
    else:
        lines.append(f"No games scheduled.")

    return "\n".join(lines)


def game_checker(preferences):
    """
    Function to check if the selected teams are playing this week and display the games.
    
    Args:
        preferences (dict): User preferences containing favorite teams and leagues

    Returns:
        str: Summary of games for this week
    """
    if not preferences:
        return "No preferences provided."

    all_weekly_games = []
    all_games_summary = []

    for league_key in SUPPORTED_LEAGUES.keys():
        team_key = f"{league_key}_team"

        if team_key in preferences and preferences[team_key]:
            favorite_teams = preferences[team_key]
            weekly_games = check_games_this_week(favorite_teams, league_key)
            
            for date, games_for_date in weekly_games.items():
                all_weekly_games.extend(games_for_date)

    display_games(all_weekly_games)

    all_games_summary.append(build_games_summary(all_weekly_games, "This Week's Games:"))

    return "\n".join(all_games_summary)