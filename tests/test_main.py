from unittest import mock
import sys
import pytest
import main

@pytest.mark.unit
def test_get_preferences_valid_nba_team():
    """Unit test for valid NBA team abbreviation."""
    args = mock.Mock()
    args.sport = "1"
    args.nba_teams = "lal"
    
    preferences = main.get_preferences(args)
    assert preferences == {"sport": "1", "nba_team": ["lal"]}


@pytest.mark.unit
def test_get_preferences_multiple_nba_teams():
    """Unit test for multiple valid NBA teams."""
    args = mock.Mock()
    args.sport = "1"
    args.nba_teams = "lal,bos"
    
    preferences = main.get_preferences(args)
    assert preferences == {"sport": "1", "nba_team": ["lal", "bos"]}
    

@pytest.mark.unit
@mock.patch('main.game_checker')
def test_main_cli_mlb_multiple_teams(mock_game_checker, capsys):
    """Unit test for multiple valid MLB teams."""
    test_args = ["--sport", "3", "--mlb-teams", "lad,nyy"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "Welcome to Friday Night Bytes!" in out
    assert "'mlb_team': ['lad', 'nyy']" in out
    mock_game_checker.assert_called_once()


@pytest.mark.unit
@mock.patch('main.game_checker')
def test_main_cli_nfl_multiple_teams(mock_game_checker, capsys):
    """Unit test for multiple valid NFL teams."""
    test_args = ["--sport", "2", "--nfl-teams", "phi,kc"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "Welcome to Friday Night Bytes!" in out
    assert "'nfl_team': ['phi', 'kc']" in out
    mock_game_checker.assert_called_once()


@pytest.mark.unit
def test_get_preferences_invalid_nba_team(capsys):
    """Unit test for invalid NBA team abbreviation."""
    args = mock.Mock()
    args.sport = "1"
    args.nba_teams = "abc"
    
    preferences = main.get_preferences(args)
    captured = capsys.readouterr()
    assert preferences is None
    assert "abc is not valid Basketball (NBA) team abbreviation(s)." in captured.out


@pytest.mark.unit
def test_get_preferences_one_invalid_nba_team(capsys):
    """Unit test for one invalid NBA team abbreviation."""
    args = mock.Mock()
    args.sport = "1"
    args.nba_teams = "lal,abc"
    
    preferences = main.get_preferences(args)
    captured = capsys.readouterr()
    assert preferences is None
    assert "abc is not valid Basketball (NBA) team abbreviation(s)." in captured.out


@pytest.mark.unit
def test_get_preferences_no_args():
    """Unit test for no arguments."""
    assert main.get_preferences(None) is None


@pytest.mark.unit
def test_get_preferences_no_sport():
    """Unit test for no sport argument."""
    args = mock.Mock()
    args.sport = None
    assert main.get_preferences(args) is None


@pytest.mark.unit
def test_get_preferences_no_teams(capsys):
    """Unit test for sport but no teams."""
    args = mock.Mock()
    args.sport = "1"
    args.nba_teams = None
    
    preferences = main.get_preferences(args)
    captured = capsys.readouterr()
    assert preferences is None
    assert "No Basketball (NBA) teams specified" in captured.out


@pytest.mark.unit
@mock.patch('main.game_checker')
def test_main_cli_short_args(mock_game_checker, capsys):
    test_args = ["-s", "1", "--nba-teams", "lal"]

    main.main(test_args)
    out = capsys.readouterr().out

    assert "Welcome to Friday Night Bytes!" in out
    assert "'nba_team': ['lal']" in out
    assert "Laker Nation" in out
    mock_game_checker.assert_called_once()


@pytest.mark.unit
@mock.patch('main.game_checker')
def test_main_cli_valid_team(mock_game_checker, capsys):
    test_args = ["--sport", "1", "--nba-teams", "lal"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "Welcome to Friday Night Bytes!" in out
    assert "'nba_team': ['lal']" in out
    assert "Laker Nation" in out
    mock_game_checker.assert_called_once()


@pytest.mark.unit
def test_main_cli_invalid_team(capsys):
    test_args = ["--sport", "1", "--nba-teams", "abc"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "abc is not valid Basketball (NBA) team abbreviation(s)." in out
    assert "When using CLI mode, both --sport and team flags are required." in out


@pytest.mark.unit
def test_main_cli_no_args(capsys):
    test_args = []
    
    with mock.patch('builtins.input', side_effect=KeyboardInterrupt()) as mock_input:
        main.main(test_args)
    
    out = capsys.readouterr().out
    
    assert "Welcome to Friday Night Bytes!" in out
    assert "Currently, the following sports are supported:" in out
    assert "1 - Basketball (NBA)" in out
    mock_input.assert_called_with("Please enter the number corresponding to your favorite sport: ")


@pytest.mark.unit
def test_main_cli_one_invalid_team(capsys):
    test_args = ["--sport", "1", "--nba-teams", "lal,abc"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "abc is not valid Basketball (NBA) team abbreviation(s)." in out
    assert "When using CLI mode, both --sport and team flags are required." in out


@pytest.mark.unit
def test_main_cli_multiple_sports(capsys):
    """Test that multiple sport team flags are rejected."""
    test_args = ["--sport", "1", "--nba-teams", "lal", "--mlb-teams", "lad"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "Error: You can only specify teams for one sport at a time." in out
    assert "Please choose either --nba-teams, --nfl-teams, or --mlb-teams, but not multiple." in out


@pytest.mark.unit
def test_main_cli_sport_but_no_teams(capsys):
    """Test that sport flag without teams is rejected."""
    test_args = ["--sport", "1"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "No Basketball (NBA) teams specified" in out
    assert "When using CLI mode, both --sport and team flags are required." in out


@pytest.mark.unit
def test_main_cli_teams_but_no_sport(capsys):
    """Test that team flags without sport is rejected."""
    test_args = ["--nba-teams", "lal"]
    
    main.main(test_args)
    out = capsys.readouterr().out
    
    assert "When using CLI mode, both --sport and team flags are required." in out


@pytest.mark.unit
def test_get_preferences_unsupported_sport(capsys):
    """Test unsupported sport number."""
    args = mock.Mock()
    args.sport = "5"
    args.nba_teams = "lal"
    
    preferences = main.get_preferences(args)
    captured = capsys.readouterr()
    assert preferences is None
    assert "Sport 5 is not supported." in captured.out