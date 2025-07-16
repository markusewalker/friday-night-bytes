from sportsipy.nba.teams import Teams
from constants import SUPPORTED_LEAGUES
from game_checker import daily_game_checker
import argparse

def get_preferences(args=None):
    """ Get user preferences for favorite sport and favorite teams. """
    if args and args.sport:
        supported_leagues = {
            "1": "nba"
            # "2": "nfl",
            # "3": "mlb",
            # "4": "mls"
        }

        league_key = supported_leagues.get(args.sport)
        if not league_key or league_key not in SUPPORTED_LEAGUES:
            print(f"Sport {args.sport} is not supported.")
            return None
        
        team_abbreviations = [abbr.lower() for _, abbr in SUPPORTED_LEAGUES[league_key]["teams"]]
        
        team_arg = getattr(args, f"{league_key}_teams", None)
        if team_arg:
            favorite_teams = [abbr.strip().lower() for abbr in team_arg.split(",")]
            invalid_teams = [team for team in favorite_teams if team not in team_abbreviations]
            if invalid_teams:
                league_name = SUPPORTED_LEAGUES[league_key]["name"]
                print(f"{', '.join(invalid_teams)} {'is' if len(invalid_teams)==1 else 'are'} not valid {league_name} team abbreviation(s).")
                return None
            
            return {
                "sport": args.sport,
                f"{league_key}_team": favorite_teams,
            }
    
    return None

def display_league_teams(league_key):
    """Display all teams for the specified league."""
    if league_key not in SUPPORTED_LEAGUES:
        return
    
    league_info = SUPPORTED_LEAGUES[league_key]
    print(f"{league_info['name']} teams:")
    
    for name, abbr in league_info["teams"]:
        print(f"{name} ({abbr})")

def get_team_input_for_league(league_key):
    """Get team input from user for the specified league."""
    if league_key not in SUPPORTED_LEAGUES:
        return []
    
    league_info = SUPPORTED_LEAGUES[league_key]
    team_abbreviations = [abbr.lower() for _, abbr in league_info["teams"]]
    
    print("\nYou can pick multiple teams by separating abbreviations with commas (e.g., lal, bos, mia).")
    while True:
        prompt = f"Please type the abbreviation(s) of your favorite {league_info['name']} team(s): "
        favorite_teams_input = input(prompt).lower()
        favorite_teams = [abbr.strip() for abbr in favorite_teams_input.split(",")]
        invalid_teams = [team for team in favorite_teams if team not in team_abbreviations]

        if not invalid_teams:
            break

        print(f"{', '.join(invalid_teams)} {'is' if len(invalid_teams)==1 else 'are'} not valid {league_info['name']} team abbreviation(s). Please try again.")
    
    return favorite_teams

def main(argv=None):
    parser = argparse.ArgumentParser(description="Friday Night Bytes CLI")
    parser.add_argument("--sport", "-s", help="Favorite sport number (e.g., 1 for NBA)")
    parser.add_argument("--nba-teams", help="Comma-separated NBA team abbreviations (e.g., lal,bos,mia)")
    # parser.add_argument("--nfl-teams", help="Comma-separated NFL team abbreviations")
    # parser.add_argument("--mlb-teams", help="Comma-separated MLB team abbreviations")
    # parser.add_argument("--mls-teams", help="Comma-separated MLS team abbreviations")
    args = parser.parse_args(argv)

    preferences = get_preferences(args) if args.sport else None

    if preferences:
        print("Welcome to Friday Night Bytes!")
        print("Stored preferences:", preferences)

        if "nba_team" in preferences and "lal" in preferences["nba_team"]:
            print("\nBleed purple and gold 💜💛! Laker Nation, stand up!")
        
        daily_game_checker(preferences)
        return

    print("Welcome to Friday Night Bytes!")
    print("Currently, the following sports are supported:")
    
    for i, (league_key, league_info) in enumerate(SUPPORTED_LEAGUES.items(), 1):
        print(f"{i} - {league_info['name']}")
    
    try:
        favorite_sport = input("Please enter the number corresponding to your favorite sport: ")
        supported_leagues = {
            "1": "nba"
            # "2": "nfl", 
            # "3": "mlb",
            # "4": "mls"
        }

        league_key = supported_leagues.get(favorite_sport)

        if not league_key or league_key not in SUPPORTED_LEAGUES:
            print("Currently, only NBA is supported.")
            return
        
        display_league_teams(league_key)        
        favorite_teams = get_team_input_for_league(league_key)
        
        if league_key == "nba" and "lal" in favorite_teams:
            print("Bleed purple and gold 💜💛! Laker Nation, stand up!")
            
        preferences = {
            "sport": favorite_sport,
            f"{league_key}_team": favorite_teams,
        }
        
        print(f"Stored preferences: {preferences}")
        daily_game_checker(preferences)
        
    except KeyboardInterrupt:
        print("\nReceived keyboard interruption. Exiting the program.")


if __name__ == "__main__":
    main()