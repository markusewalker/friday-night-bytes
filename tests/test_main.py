from unittest import mock
import sys
import pytest
import main

MOCK_NBA_TEAMS = [
    mock.Mock(name="Los Angeles Lakers", abbreviation="LAL"),
    mock.Mock(name="Boston Celtics", abbreviation="BOS"),
    mock.Mock(name="Golden State Warriors", abbreviation="GSW"),
    mock.Mock(name="Houston Rockets", abbreviation="HOU"),
]

@pytest.mark.unit
@mock.patch('main.Teams')
def test_get_preferences_valid_nba_team(mock_teams):
    """Unit test for valid NBA team abbreviation."""
    mock_teams.return_value = MOCK_NBA_TEAMS
    
    args = mock.Mock()
    args.sport = "1"
    args.nba_teams = "lal"
    
    preferences = main.get_preferences(args)
    assert preferences == {"sport": "1", "nba_team": ["lal"]}

@pytest.mark.unit
@mock.patch('main.Teams')
def test_get_preferences_multiple_nba_teams(mock_teams):
    """Unit test for multiple valid NBA team abbreviations."""
    mock_teams.return_value = MOCK_NBA_TEAMS
    
    args = mock.Mock()
    args.sport = "1"
    args.nba_teams = "lal,bos"
    
    preferences = main.get_preferences(args)
    assert preferences == {"sport": "1", "nba_team": ["lal", "bos"]}

@pytest.mark.unit
@mock.patch('main.Teams')
def test_get_preferences_invalid_nba_team(mock_teams, capsys):
    """Unit test for invalid NBA team abbreviation."""
    mock_teams.return_value = MOCK_NBA_TEAMS
    
    args = mock.Mock()
    args.sport = "1"
    args.nba_teams = "abc"
    
    preferences = main.get_preferences(args)
    captured = capsys.readouterr()
    assert preferences is None
    assert "abc is not valid Basketball (NBA) team abbreviation(s)." in captured.out
    
@pytest.mark.unit
@mock.patch('main.Teams')
def test_get_preferences_one_invalid_nba_team(mock_teams, capsys):
    """Unit test for one invalid NBA team abbreviation."""
    mock_teams.return_value = MOCK_NBA_TEAMS
    
    args = mock.Mock()
    args.sport = "1"
    args.nba_teams = "lal,abc"
    
    preferences = main.get_preferences(args)
    captured = capsys.readouterr()
    assert preferences is None
    assert "abc is not valid Basketball (NBA) team abbreviation(s)." in captured.out

@pytest.mark.unit
@mock.patch('main.Teams')
def test_get_preferences_no_args(mock_teams):
    """Unit test for no arguments."""
    mock_teams.return_value = MOCK_NBA_TEAMS
    assert main.get_preferences(None) is None
    
@pytest.mark.unit
@mock.patch('main.Teams')
def test_main_cli_short_args(mock_teams, capsys):
    test_args = ["-s", "1", "--nba-teams", "lal"]

    main.main(test_args)
    out = capsys.readouterr().out

    assert "Welcome to Friday Night Bytes!" in out
    assert "'nba_team': ['lal']" in out
    assert "Laker Nation" in out

@pytest.mark.unit
@mock.patch('main.Teams')
def test_main_cli_valid_team(mock_teams, capsys):
    test_args = ["--sport", "1", "--nba-teams", "lal"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "Welcome to Friday Night Bytes!" in out
    assert "'nba_team': ['lal']" in out
    assert "Laker Nation" in out
    
@pytest.mark.unit
@mock.patch('main.Teams')
@mock.patch('builtins.input', side_effect=KeyboardInterrupt())
def test_main_cli_invalid_team(mock_input, mock_teams, capsys):
    test_args = ["--sport", "1", "--nba-teams", "abc"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "abc is not valid Basketball (NBA) team abbreviation(s)." in out
    assert "Welcome to Friday Night Bytes!" in out
    
@pytest.mark.unit
@mock.patch('main.Teams')
def test_main_cli_no_args(mock_teams, capsys):
    test_args = []
    
    with mock.patch('builtins.input', side_effect=KeyboardInterrupt()) as mock_input:
        main.main(test_args)
    
    out = capsys.readouterr().out
    
    assert "Welcome to Friday Night Bytes!" in out
    assert "Currently, the following sports are supported:" in out
    assert "1 - Basketball (NBA)" in out
    mock_input.assert_called_with("Please enter the number corresponding to your favorite sport: ")
    
@pytest.mark.unit
@mock.patch('main.Teams')
@mock.patch('builtins.input', side_effect=KeyboardInterrupt())
def test_main_cli_one_invalid_team(mock_input, mock_teams, capsys):
    test_args = ["--sport", "1", "--nba-teams", "lal,abc"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "abc is not valid Basketball (NBA) team abbreviation(s)." in out
    assert "Welcome to Friday Night Bytes!" in out