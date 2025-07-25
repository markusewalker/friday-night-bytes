from constants import SUPPORTED_LEAGUES
from gamechecker.game_checker import game_checker
from gui.gui_app import main as gui_main
import argparse, os

def get_preferences(args=None):
    """ Get user preferences for favorite sport and favorite teams. """
    if not args or not args.sport:
        return None
        
    supported_leagues = {
        "1": "nba",
        "2": "nfl",
        "3": "mlb",
    }

    league_key = supported_leagues.get(args.sport)
    if not league_key or league_key not in SUPPORTED_LEAGUES:
        print(f"Sport {args.sport} is not supported.")
        return None
    
    team_abbreviations = [abbr.lower() for _, abbr in SUPPORTED_LEAGUES[league_key]["teams"]]
    
    team_arg = getattr(args, f"{league_key}_teams", None)
    if not team_arg:
        league_name = SUPPORTED_LEAGUES[league_key]["name"]
        print(f"No {league_name} teams specified. Please provide team abbreviations using --{league_key}-teams.")

        return None
        
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
    parser.add_argument("--sport", "-s", help="Favorite sport number (i.e. 1 for NBA, 2 for NFL, 3 for MLB)")
    parser.add_argument("--nba-teams", help="Comma-separated NBA team abbreviations (i.e. lal,bos,mia)")
    parser.add_argument("--nfl-teams", help="Comma-separated NFL team abbreviations (i.e. phi,kc,sf)")
    parser.add_argument("--mlb-teams", help="Comma-separated MLB team abbreviations (i.e. lad, nyy, bos)")
    parser.add_argument("--gui", action="store_true", help="Launch the GUI version")
    args = parser.parse_args(argv)

    if args.gui:
        try:
            gui_main()
            return
        except ImportError as e:
            print(f"GUI mode is not available: {e}")
            print("Please ensure tkinter and Pillow are installed.")
            return

    using_cli = args.sport or args.nba_teams or args.nfl_teams or args.mlb_teams
    
    if using_cli:
        team_flags_provided = sum([bool(args.nba_teams), bool(args.nfl_teams), bool(args.mlb_teams)])
        if team_flags_provided > 1:
            print("Error: You can only specify teams for one sport at a time.")
            print("Please choose either --nba-teams, --nfl-teams, or --mlb-teams, but not multiple.")
            print("\nUsage: python main.py --sport <sport_number> --<league>-teams <team_abbreviations>")
            print("Example: python main.py --sport 1 --nba-teams lal,bos")
            print("Example: python main.py --sport 3 --mlb-teams lad,nyy")
            return
        
        preferences = get_preferences(args)
        if preferences:
            print("Welcome to Friday Night Bytes!")
            print(f"Preferences: {preferences}")

            if "nba_team" in preferences and "lal" in preferences["nba_team"]:
                print("\nBleed purple and gold 💜💛! Laker Nation, stand up!")
            
            game_checker(preferences)
        else:
            print("When using CLI mode, both --sport and team flags are required.")
            print("Usage: python main.py --sport <sport_number> --<league>-teams <team_abbreviations>")
            print("Example: python main.py --sport 1 --nba-teams lal,bos")
            print("Example: python main.py --sport 3 --mlb-teams lad,nyy")
            print("\nSupported sports:")
            for i, (league_key, league_info) in enumerate(SUPPORTED_LEAGUES.items(), 1):
                print(f"  {i} - {league_info['name']}")
        return

    print("Welcome to Friday Night Bytes!")
    print("Currently, the following sports are supported:")
    
    for i, (league_key, league_info) in enumerate(SUPPORTED_LEAGUES.items(), 1):
        print(f"{i} - {league_info['name']}")
    
    try:
        favorite_sport = input("Please enter the number corresponding to your favorite sport: ")
        supported_leagues = {
            "1": "nba",
            "2": "nfl",
            "3": "mlb",
        }

        league_key = supported_leagues.get(favorite_sport)

        if not league_key or league_key not in SUPPORTED_LEAGUES:
            print(f"{favorite_sport} is not supported...")
            return
        
        display_league_teams(league_key)        
        favorite_teams = get_team_input_for_league(league_key)
        
        if league_key == "nba" and "lal" in favorite_teams:
            print("Bleed purple and gold 💜💛! Laker Nation, stand up!")
            
        preferences = {
            "sport": favorite_sport,
            f"{league_key}_team": favorite_teams,
        }

        game_checker(preferences)

    except KeyboardInterrupt:
        print("\nReceived keyboard interruption. Exiting the program.")


if __name__ == "__main__":
    main()