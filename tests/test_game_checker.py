from gamechecker.game_checker import display_games_today
from datetime import date
import pytest


@pytest.mark.unit
def test_game_display_with_game():
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
            'time': '8:00 PM EST',
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
            'time': '10:30 PM EST',
            'date': date.today().strftime('%Y-%m-%d')
        }
    ]
    
    print("=" * 50)
    display_games_today(mock_games)
    
@pytest.mark.unit
def test_game_display_no_games():
    """Test the game display functionality with no games."""
    print("=" * 50)
    display_games_today([])