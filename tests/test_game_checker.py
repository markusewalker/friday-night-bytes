from gamechecker.game_checker import display_games_today, display_games_tomorrow
from datetime import date
import pytest


@pytest.mark.unit
def test_game_display_with_nba_game():
    """Test the game display functionality with a mock game."""
    
    mock_games = [
        {
            'league': 'nba',
            'league_name': 'Basketball (NBA)',
            'team': 'Los Angeles Lakers',
            'team_abbr': 'LAL',
            'opponent': 'Boston Celtics',
            'opponent_abbr': 'BOS',
            'is_home': True,
            'date': date.today().strftime('%Y-%m-%d')
        },
        {
            'league': 'nba',
            'league_name': 'Basketball (NBA)',
            'team': 'Miami Heat',
            'team_abbr': 'MIA',
            'opponent': 'Golden State Warriors',
            'opponent_abbr': 'GSW',
            'is_home': False,
            'date': date.today().strftime('%Y-%m-%d')
        }
    ]
    
    print("=" * 50)
    display_games_today(mock_games)
    

@pytest.mark.unit
def test_game_display_with_nfl_game():
    """Test the game display functionality with a mock NFL game."""
    
    mock_games = [
        {
            'league': 'nfl',
            'league_name': 'Football (NFL)',
            'team': 'Los Angeles Rams',
            'team_abbr': 'LAR',
            'opponent': 'San Francisco 49ers',
            'opponent_abbr': 'SF',
            'is_home': True,
            'date': date.today().strftime('%Y-%m-%d')
        }
    ]
    
    print("=" * 50)
    display_games_today(mock_games)
    

@pytest.mark.unit
def test_game_display_with_mlb_game():
    """Test the game display functionality with a mock MLB game."""
    
    mock_games = [
        {
            'league': 'mlb',
            'league_name': 'Baseball (MLB)',
            'team': 'New York Yankees',
            'team_abbr': 'NYY',
            'opponent': 'Boston Red Sox',
            'opponent_abbr': 'BOS',
            'is_home': False,
            'date': date.today().strftime('%Y-%m-%d')
        }
    ]
    
    print("=" * 50)
    display_games_today(mock_games)


@pytest.mark.unit
def test_game_display_no_games_today():
    """Test the game display functionality with no games."""
    print("=" * 50)
    display_games_today([])
    

@pytest.mark.unit
def test_game_display_no_games_tomorrow():
    """Test the game display functionality with no games for tomorrow."""
    print("=" * 50)
    display_games_tomorrow([])