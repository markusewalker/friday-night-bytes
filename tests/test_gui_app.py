from gui.gui_app import FridayNightBytesGUI
from constants import SUPPORTED_LEAGUES
from unittest.mock import Mock, patch
import unittest
import unittest.mock as mock
import pytest
import tkinter as tk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestFridayNightBytesGUI(unittest.TestCase):
    """Test suite for FridayNightBytesGUI class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_root = Mock()
        self.mock_root.winfo_children.return_value = []
        self.mock_root.winfo_screenwidth.return_value = 1920
        self.mock_root.winfo_screenheight.return_value = 1080
        self.mock_root._last_child_ids = {}
        self.mock_root.tk = Mock()
        self.mock_root._w = "."
        
        with patch('gui.gui_app.tk.Tk', return_value=self.mock_root), \
             patch('gui.gui_app.tk.Frame'), \
             patch('gui.gui_app.tk.Label'), \
             patch('gui.gui_app.tk.Button'), \
             patch('gui.gui_app.tk.Canvas'), \
             patch('gui.gui_app.ttk.Scrollbar'), \
             patch('gui.gui_app.tk.Text'), \
             patch('gui.gui_app.Image'), \
             patch('gui.gui_app.ImageTk'), \
             patch.object(FridayNightBytesGUI, 'show_splash_screen'):
            self.gui = FridayNightBytesGUI()

    @pytest.mark.unit
    def test_init(self):
        """Test GUI initialization."""
        self.mock_root.title.assert_called_with("Friday Night Bytes")
        self.mock_root.geometry.assert_called()
        self.mock_root.configure.assert_called_with(bg="#16213e")
        
        self.assertIsNone(self.gui.selected_sport)
        self.assertEqual(self.gui.selected_teams, [])

    @pytest.mark.unit
    def test_center_window(self):
        """Test window centering functionality."""
        self.mock_root.winfo_screenwidth.return_value = 1920
        self.mock_root.winfo_screenheight.return_value = 1080
        
        self.gui.center_window()
        self.mock_root.update_idletasks.assert_called()
        self.assertTrue(self.mock_root.geometry.called)

    @pytest.mark.unit
    def test_clear_window(self):
        """Test window clearing functionality."""
        mock_widget1 = Mock()
        mock_widget2 = Mock()
        self.mock_root.winfo_children.return_value = [mock_widget1, mock_widget2]
        
        self.gui.clear_window()
        
        mock_widget1.destroy.assert_called_once()
        mock_widget2.destroy.assert_called_once()

    @pytest.mark.unit
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Label')
    @patch('os.path.exists')
    def test_show_splash_screen_with_logo(self, mock_exists, mock_label, mock_frame):
        """Test splash screen display with logo."""
        mock_exists.return_value = True
        
        with patch('gui.gui_app.Image.open') as mock_image, \
             patch('gui.gui_app.ImageTk.PhotoImage') as mock_photo:
            
            mock_img = Mock()
            mock_image.return_value = mock_img
            mock_img.resize.return_value = mock_img
            
            self.gui.show_splash_screen()
            
            mock_image.assert_called()
            mock_img.resize.assert_called()
            mock_photo.assert_called()

    @pytest.mark.unit
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Label')
    @patch('os.path.exists')
    def test_show_splash_screen_without_logo(self, mock_exists, mock_label, mock_frame):
        """Test splash screen display without logo."""
        mock_exists.return_value = False
        
        self.gui.show_splash_screen()

        mock_frame.assert_called()
        mock_label.assert_called()

    @pytest.mark.unit
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Label')
    def test_show_sport_selection(self, mock_label, mock_frame):
        """Test sport selection screen display."""
        with patch.object(self.gui, 'create_sport_button') as mock_create:
            self.gui.show_sport_selection()
            
            expected_calls = [
                mock.call(mock.ANY, "nba", "🏀", 0),
                mock.call(mock.ANY, "nfl", "🏈", 1),
                mock.call(mock.ANY, "mlb", "⚾", 2)
            ]
            mock_create.assert_has_calls(expected_calls)

    @pytest.mark.unit
    def test_select_sport(self):
        """Test sport selection functionality."""
        with patch.object(self.gui, 'show_team_selection') as mock_show_teams:
            self.gui.select_sport("nba")
            
            self.assertEqual(self.gui.selected_sport, "nba")
            mock_show_teams.assert_called_once()

    @pytest.mark.unit
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Label')
    @patch('gui.gui_app.tk.Button')
    @patch('gui.gui_app.tk.Canvas')
    @patch('gui.gui_app.ttk.Scrollbar')
    def test_show_team_selection_valid_sport(self, mock_scrollbar, mock_canvas, mock_button, mock_label, mock_frame):
        """Test team selection screen for valid sport."""
        self.gui.selected_sport = "nba"
        
        mock_canvas_instance = Mock()
        mock_canvas_instance.winfo_width.return_value = 600
        mock_canvas.return_value = mock_canvas_instance
        
        with patch.object(self.gui, 'create_team_button') as mock_create_team:
            self.gui.show_team_selection()
            
            self.assertEqual(self.gui.selected_teams, [])
            
            nba_teams = SUPPORTED_LEAGUES["nba"]["teams"]
            self.assertEqual(mock_create_team.call_count, len(nba_teams))

    @pytest.mark.unit
    def test_show_team_selection_invalid_sport(self):
        """Test team selection screen for invalid sport."""
        self.gui.selected_sport = "invalid"
        
        with patch.object(self.gui, 'show_sport_selection') as mock_show_sport:
            self.gui.show_team_selection()
            
            mock_show_sport.assert_called_once()

    @pytest.mark.unit
    def test_toggle_team_select(self):
        """Test team selection toggle - selecting a team."""
        mock_button = Mock()
        mock_button.cget.return_value = "Team Name (ABC)"
        self.gui.team_buttons = {"ABC": mock_button}
        self.gui.selected_teams = []
        
        self.gui.continue_btn = Mock()
        self.gui.continue_btn.winfo_viewable.return_value = False
        
        self.gui.toggle_team("ABC")
        self.assertIn("abc", self.gui.selected_teams)
        mock_button.config.assert_called_with(bg="#ac9c7c")

    @pytest.mark.unit
    def test_toggle_team_deselect(self):
        """Test team selection toggle - deselecting a team."""
        mock_button = Mock()
        mock_button.cget.return_value = "Team Name (ABC)"

        self.gui.team_buttons = {"ABC": mock_button}
        self.gui.selected_teams = ["abc"]
        
        self.gui.continue_btn = Mock()
        self.gui.continue_btn.winfo_viewable.return_value = True
        self.gui.toggle_team("ABC")
        self.assertNotIn("abc", self.gui.selected_teams)
        
        mock_button.config.assert_called_with(bg="#ffffff")

    @pytest.mark.unit
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Button')
    @patch('os.path.exists')
    def test_create_team_button_with_logo(self, mock_exists, mock_button, mock_frame):
        """Test team button creation with logo."""
        mock_exists.return_value = True
        self.gui.selected_sport = "nba"
        self.gui.cols_per_row = 4
        self.gui.team_buttons = {}
        
        mock_parent = Mock()
        
        with patch('gui.gui_app.Image.open') as mock_image, \
             patch('gui.gui_app.ImageTk.PhotoImage') as mock_photo:
            
            mock_img = Mock()
            mock_image.return_value = mock_img
            mock_img.resize.return_value = mock_img
            
            self.gui.create_team_button(mock_parent, "Test Team", "TST", 0)
            
            mock_image.assert_called()
            mock_img.resize.assert_called_with((80, 80), mock.ANY)

    @pytest.mark.unit
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Button')
    @patch('os.path.exists')
    def test_create_team_button_without_logo(self, mock_exists, mock_button, mock_frame):
        """Test team button creation without logo."""
        mock_exists.return_value = False
        self.gui.selected_sport = "nba"
        self.gui.cols_per_row = 4
        self.gui.team_buttons = {}
        
        mock_parent = Mock()
        
        self.gui.create_team_button(mock_parent, "Test Team", "TST", 0)        
        mock_button.assert_called()

    @pytest.mark.unit
    @patch('gui.gui_app.messagebox.showwarning')
    def test_show_games_no_teams_selected(self, mock_warning):
        """Test show games with no teams selected."""
        self.gui.selected_teams = []
        self.gui.show_games()
        mock_warning.assert_called_with("No Teams Selected", "Please select at least one team.")

    @pytest.mark.unit
    def test_show_games_no_sport_selected(self):
        """Test show games with no sport selected."""
        self.gui.selected_teams = ["lal"]
        self.gui.selected_sport = None
        
        with patch.object(self.gui, 'show_sport_selection') as mock_show_sport:
            self.gui.show_games()
            mock_show_sport.assert_called_once()

    @pytest.mark.unit
    @patch('gui.gui_app.game_checker')
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Label')
    def test_show_games_success(self, mock_label, mock_frame, mock_game_checker):
        """Test successful game display."""
        self.gui.selected_teams = ["lal"]
        self.gui.selected_sport = "nba"

        mock_game_checker.return_value = None
        
        with patch.object(self.gui, 'show_games_result') as mock_show_result:
            self.gui.show_games()
            
            expected_preferences = {
                "sport": "1",
                "nba_team": ["lal"]
            }

            mock_game_checker.assert_called_with(expected_preferences)

    @pytest.mark.unit
    @patch('gui.gui_app.game_checker')
    @patch('gui.gui_app.messagebox.showerror')
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Label')
    def test_show_games_error(self, mock_label, mock_frame, mock_error, mock_game_checker):
        """Test game display with error."""
        self.gui.selected_teams = ["lal"]
        self.gui.selected_sport = "nba"

        mock_game_checker.side_effect = Exception("Test error")
        
        with patch.object(self.gui, 'show_team_selection') as mock_show_teams:
            self.gui.show_games()
            
            mock_error.assert_called_with("Error", "An error occurred while fetching games: Test error")
            mock_show_teams.assert_called_once()

    @pytest.mark.unit
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Button')
    @patch('gui.gui_app.tk.Label')
    @patch('gui.gui_app.tk.Text')
    @patch('gui.gui_app.ttk.Scrollbar')
    def test_show_games_result(self, mock_scrollbar, mock_text, mock_label, mock_button, mock_frame):
        """Test games result display."""
        test_output = "Test game output"
        
        self.gui.show_games_result(test_output)
        mock_text.assert_called()
        
        text_instance = mock_text.return_value
        text_instance.insert.assert_called_with("1.0", test_output)
        text_instance.config.assert_called_with(state="disabled")

    @pytest.mark.unit
    def test_run(self):
        """Test GUI run method."""
        self.gui.run()
        self.mock_root.mainloop.assert_called_once()


class TestFridayNightBytesGUIIntegration(unittest.TestCase):
    """Integration tests for GUI workflow."""
    
    @pytest.mark.integration
    @patch('gui.gui_app.tk.Tk')
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Label') 
    @patch('gui.gui_app.tk.Button')
    @patch.object(FridayNightBytesGUI, 'show_splash_screen')
    def test_sport_to_team_selection_workflow(self, mock_splash, mock_button, mock_label, mock_frame, mock_tk):
        """Test workflow from sport selection to team selection."""
        mock_root = Mock()
        mock_root.winfo_screenwidth.return_value = 1920
        mock_root.winfo_screenheight.return_value = 1080
        mock_root._last_child_ids = {}
        mock_root.tk = Mock()
        mock_tk.return_value = mock_root
        
        gui = FridayNightBytesGUI()
        
        with patch.object(gui, 'show_team_selection') as mock_show_teams:
            gui.select_sport("nba")
            
            self.assertEqual(gui.selected_sport, "nba")
            mock_show_teams.assert_called_once()

    @pytest.mark.integration
    @patch('gui.gui_app.tk.Tk')
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Label')
    @patch('gui.gui_app.tk.Button')
    @patch.object(FridayNightBytesGUI, 'show_splash_screen')
    def test_team_selection_workflow(self, mock_splash, mock_button, mock_label, mock_frame, mock_tk):
        """Test team selection and game viewing workflow."""
        mock_root = Mock()
        mock_root.winfo_screenwidth.return_value = 1920
        mock_root.winfo_screenheight.return_value = 1080
        mock_root._last_child_ids = {}
        mock_root.tk = Mock()
        mock_tk.return_value = mock_root
        
        gui = FridayNightBytesGUI()
        gui.selected_sport = "nba"
        gui.team_buttons = {"LAL": Mock()}
        gui.continue_btn = Mock()
        gui.continue_btn.winfo_viewable.return_value = False
        
        gui.toggle_team("LAL")
        self.assertIn("lal", gui.selected_teams)
        
        gui.continue_btn.pack.assert_called()

    @pytest.mark.integration
    @patch('gui.gui_app.tk.Tk')
    @patch('gui.gui_app.tk.Frame')
    @patch('gui.gui_app.tk.Label')
    @patch('gui.gui_app.tk.Button')
    @patch('gui.gui_app.tk.Canvas')
    @patch('gui.gui_app.ttk.Scrollbar')
    @patch('gui.gui_app.game_checker')
    @patch.object(FridayNightBytesGUI, 'show_splash_screen')
    def test_full_workflow_integration(self, mock_splash, mock_game_checker, mock_scrollbar, mock_canvas, mock_button, mock_label, mock_frame, mock_tk):
        """Test complete workflow integration."""
        mock_root = Mock()
        mock_root.winfo_children.return_value = []
        mock_root.winfo_screenwidth.return_value = 1920
        mock_root.winfo_screenheight.return_value = 1080
        mock_root._last_child_ids = {}
        mock_root._w = "."
        mock_root.tk = Mock()
        mock_tk.return_value = mock_root
        mock_game_checker.return_value = None
        
        mock_canvas_instance = Mock()
        mock_canvas_instance.winfo_width.return_value = 600
        mock_canvas.return_value = mock_canvas_instance
        
        gui = FridayNightBytesGUI()
        
        with patch.object(gui, 'show_team_selection'):
            gui.select_sport("nba")
            self.assertEqual(gui.selected_sport, "nba")
        
        gui.team_buttons = {"LAL": Mock()}
        gui.continue_btn = Mock()
        gui.continue_btn.winfo_viewable.return_value = False
        
        gui.toggle_team("LAL")
        self.assertIn("lal", gui.selected_teams)
        
        with patch.object(gui, 'show_games_result') as mock_result:
            gui.show_games()
            
            expected_preferences = {
                "sport": "1",
                "nba_team": ["lal"]
            }

            mock_game_checker.assert_called_with(expected_preferences)


if __name__ == '__main__':
    unittest.main()