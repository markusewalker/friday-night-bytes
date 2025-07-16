from datetime import datetime, date
from sportsipy.nba.schedule import Schedule
from constants import SUPPORTED_LEAGUES
import time
import requests

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
        return Schedule(team_abbr.upper())
    # elif league == "nfl":
    #     return NFLSchedule(team_abbr.upper())
    # elif league == "mlb":
    #     return MLBSchedule(team_abbr.upper())
    else:
        raise ValueError(f"Unsupported league: {league}")

def check_games_today(favorite_teams, league):
    """
    Check if any of the selected favorite teams have games scheduled for today.

    Args:
        favorite_teams (list): List of team abbreviations (e.g., ['lal', 'bos'])
        league (str): The league to check (e.g., 'nba', 'nfl', 'mlb') - REQUIRED
    
    Returns:
        list: List of dictionaries containing game information for today
    """
    today = date.today()
    games_today = []
    
    if not favorite_teams or league not in SUPPORTED_LEAGUES:
        return games_today
    
    league_name = SUPPORTED_LEAGUES[league]["name"]
    print(f"\nChecking for {league_name} games today...")
    
    for i, team_abbr in enumerate(favorite_teams):
        team_name = get_team_name_from_abbreviation(team_abbr, league)
        if not team_name:
            print(f"  ❌ Unknown team: {team_abbr}")
            continue
            
        print(f"  🔍 Checking for the {team_name}...")
        
        try:
            # Put a sleep between requests to avoid rate limiting
            if i > 0:
                time.sleep(5)
                
            schedule = get_schedule_for_league(team_abbr, league)
            
            team_has_game_today = False
            for game in schedule:
                try:
                    game_date = datetime.strptime(game.date, '%Y-%m-%d').date()
                except (ValueError, AttributeError):
                    continue
                
                if game_date == today:
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
                        'time': game.time if hasattr(game, 'time') else 'TBD',
                        'date': game_date.strftime('%Y-%m-%d')
                    }
                    
                    games_today.append(game_info)
                    print(f"    ✅ Game found!")
                    team_has_game_today = True
                    break
            
            if not team_has_game_today:
                print(f"    🔴 No game today")
                    
        except requests.exceptions.HTTPError as e:
            if "429" in str(e):
                print(f"    ⚠️  Rate limit reached for {team_name}. Please try again later.")
                continue
            else:
                print(f"    ❌ HTTP error checking {team_name}: {e}")
        except Exception as e:
            print(f"    ❌ Error checking {team_name}: {e}")
            continue
    
    return games_today

def display_games_today(games_today):
    """
    Display information about games scheduled for today.
    
    Args:
        games_today (list): List of game dictionaries
    """
    if not games_today:
        print("\nThat sucks! No games are scheduled today for your favorite teams.")
        return
    
    games_by_league = {}
    for game in games_today:
        league = game['league']

        if league not in games_by_league:
            games_by_league[league] = []

        games_by_league[league].append(game)
    
    print(f"\nGames today ({date.today().strftime('%B %d, %Y')}):")
    print("-" * 50)
    
    for league, games in games_by_league.items():
        league_name = games[0]['league_name']
        print(f"\n{league_name}:")
        
        for game in games:
            if game['is_home']:
                print(f"🏠 {game['team']} vs {game['opponent']}")
            else:
                print(f"✈️  {game['team']} @ {game['opponent']}")
            
            if game['time'] != 'TBD':
                print(f"   Time: {game['time']}")
            else:
                print("   Time: To Be Determined")
            print()

def daily_game_checker(preferences):
    """
    Function to check if the selected teams are playing today and display the games.
    
    Args:
        preferences (dict): User preferences containing favorite teams and leagues
    """
    if not preferences:
        return
    
    all_games_today = []
    
    for league_key in SUPPORTED_LEAGUES.keys():
        team_key = f"{league_key}_team"

        if team_key in preferences and preferences[team_key]:
            favorite_teams = preferences[team_key]
            games_today = check_games_today(favorite_teams, league_key)
            all_games_today.extend(games_today)
    
    display_games_today(all_games_today)