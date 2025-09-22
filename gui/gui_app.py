import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamechecker.game_checker import game_checker
from constants import SUPPORTED_LEAGUES
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import tkinter as tk
import io
import contextlib

class FridayNightBytesGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Friday Night Bytes")
        self.root.geometry("800x600")
        self.root.configure(bg="#16213e")
        
        self.center_window()
        
        self.selected_sport = None
        self.selected_teams = []
        
        self.show_splash_screen()


    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")


    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()


    def show_splash_screen(self):
        """Display the splash screen for 5 seconds."""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both")
        
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")

        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((500, 500), Image.Resampling.LANCZOS)
            
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(main_frame, image=self.logo_photo, bg="#1a1a2e")
        logo_label.pack(expand=True)

        self.root.after(5000, self.show_sport_selection)


    def show_sport_selection(self):
        """Display the sport selection screen with clickable sports."""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both")
        
        title_label = tk.Label(
            main_frame,
            text="Choose Your Favorite Sport!",
            font=("Helvetica", 32, "bold"),
            fg="#eee2dc",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(30, 40))
        
        sports_frame = tk.Frame(main_frame, bg="#1a1a2e")
        sports_frame.pack(expand=True)

        self.create_sport_button(sports_frame, "nba", 0)
        self.create_sport_button(sports_frame, "nfl", 1)
        self.create_sport_button(sports_frame, "mlb", 2)


    def create_sport_button(self, parent, sport_key, row):
        """Create a clickable sport button."""
        sport_frame = tk.Frame(parent, bg="#16213e")
        sport_frame.grid(row=row//3, column=row%3, padx=20, pady=20, sticky="nsew")
        
        parent.grid_rowconfigure(row//3, weight=1)
        parent.grid_columnconfigure(row%3, weight=1)
        
        sport_frame.bind("<Button-1>", lambda e: self.select_sport(sport_key))
        
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", f"{sport_key}-logo.png")
        
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((250, 250), Image.Resampling.LANCZOS)
        sport_logo = ImageTk.PhotoImage(logo_img)
                
        logo_label = tk.Label(
            sport_frame,
            image=sport_logo,
            bg="#16213e",
            cursor="hand2"
        )
                
        if not hasattr(self, 'sport_logos'):
            self.sport_logos = {}

        self.sport_logos[sport_key] = sport_logo
        
        logo_label.pack(expand=True)
        logo_label.bind("<Button-1>", lambda e: self.select_sport(sport_key))


        def on_enter(e):
            sport_frame.config(bg="#ac9c7c")
            logo_label.config(bg="#ac9c7c")


        def on_leave(e):
            sport_frame.config(bg="#16213e")
            logo_label.config(bg="#16213e")
        
        sport_frame.bind("<Enter>", on_enter)
        sport_frame.bind("<Leave>", on_leave)
        logo_label.bind("<Enter>", on_enter)
        logo_label.bind("<Leave>", on_leave)
        
        sport_frame.config(width=400, height=300)
        sport_frame.pack_propagate(False)


    def select_sport(self, sport_key):
        """Handle sport selection."""
        self.selected_sport = sport_key
        self.show_team_selection()


    def show_team_selection(self):
        """Display the team selection screen for the chosen sport.
        
        There is a continue button that appears when teams are selected.
        
        Additionally, if you wish to go back to the sport selection,
        you can click the back button at the top left.
        """
        self.selected_teams = []
        
        self.clear_window()
        
        if not self.selected_sport or self.selected_sport not in SUPPORTED_LEAGUES:
            self.show_sport_selection()
            return
            
        league_info = SUPPORTED_LEAGUES[self.selected_sport]
        
        main_frame = tk.Frame(self.root, bg="#16213e")
        main_frame.pack(expand=True, fill="both")
        
        header_frame = tk.Frame(main_frame, bg="#16213e")
        header_frame.pack(fill="x", pady=(20, 10))
        
        back_btn = tk.Button(
            header_frame,
            text="Back",
            font=("Helvetica", 12),
            bg="#16213e",
            fg="#eee2dc",
            activebackground="#ac9c7c",
            activeforeground="#1a1a2e",
            border=0,
            padx=15,
            pady=5,
            command=self.show_sport_selection
        )
        back_btn.pack(side="left", padx=20)
        
        self.continue_btn = tk.Button(
            header_frame,
            text="View Games",
            font=("Helvetica", 12),
            bg="#16213e",
            fg="#eee2dc",
            activebackground="#ac9c7c",
            activeforeground="#1a1a2e",
            border=0,
            padx=15,
            pady=5,
            command=self.show_games
        )
        
        title_label = tk.Label(
            header_frame,
            text=f"Select Your Favorite Team(s)!",
            font=("Helvetica", 20, "bold"),
            fg="#eee2dc",
            bg="#1a1a2e",
        )
        title_label.pack(side="left", padx=(50, 0))
        
        canvas = tk.Canvas(main_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        teams_wrapper = tk.Frame(scrollable_frame, bg="#1a1a2e")
        teams_wrapper.pack(expand=True, fill="both", padx=20)
        
        teams_frame = tk.Frame(teams_wrapper, bg="#1a1a2e")
        teams_frame.pack(fill="both", expand=True, pady=20)
        
        self.team_buttons = {}        
        self.teams_frame = teams_frame
        self.teams_wrapper = teams_wrapper
        
        self.root.update_idletasks()
        canvas_width = canvas.winfo_width()

        if canvas_width <= 1:  # If canvas isn't sized yet, use a reasonable default value
            canvas_width = 600

        available_width = canvas_width - 40
        button_width = 130
        cols_per_row = max(1, available_width // button_width)
        
        self.cols_per_row = cols_per_row
        
        for i, (team_name, team_abbr) in enumerate(league_info["teams"]):
            self.create_team_button(teams_frame, team_name, team_abbr, i)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        scrollbar.pack(side="right", fill="y", padx=(0, 20))

        self.canvas = canvas

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _on_mousewheel_linux(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _on_mousewheel_up(event):
            canvas.yview_scroll(-1, "units")

        def _on_mousewheel_down(event):
            canvas.yview_scroll(1, "units")
        
        self._mousewheel_callbacks = {
            'wheel': _on_mousewheel,
            'wheel_linux': _on_mousewheel_linux,
            'up': _on_mousewheel_up,
            'down': _on_mousewheel_down
        }
        
        self._bind_mousewheel_to_widget(canvas)
        self._bind_mousewheel_to_widget(scrollable_frame)
        self._bind_mousewheel_to_widget(teams_wrapper)
        self._bind_mousewheel_to_widget(teams_frame)


    def _bind_mousewheel_to_widget(self, widget):
        """Helper method to bind mouse wheel events to a widget.
        
        Supports Windows, MacOS and Linux.
        """
        widget.bind("<MouseWheel>", self._mousewheel_callbacks['wheel'])
        widget.bind("<Button-4>", self._mousewheel_callbacks['up'])
        widget.bind("<Button-5>", self._mousewheel_callbacks['down'])


    def create_team_button(self, parent, team_name, team_abbr, index):
        """Create a clickable team button with logo."""
        cols_per_row = getattr(self, 'cols_per_row', 4)
            
        row = index // cols_per_row
        col = index % cols_per_row
        
        team_frame = tk.Frame(parent, bg="#16213e", relief="raised", bd=1)
        team_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        
        # Configure grid weights for responsive behavior
        parent.grid_columnconfigure(col, weight=1, minsize=120)
        parent.grid_rowconfigure(row, weight=1)

        sport_folder = str(self.selected_sport)
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "teamlogos", sport_folder)
        
        possible_filenames = [
            f"{team_abbr.lower()}.png",
            f"{team_name.lower().replace(' ', '_')}.png",
        ]
        
        logo_path = None
        for filename in possible_filenames:
            potential_path = os.path.join(base_path, filename)

            if os.path.exists(potential_path):
                logo_path = potential_path
                break
        
        logo_size = 80
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        team_logo = ImageTk.PhotoImage(logo_img)
            
        team_btn = tk.Button(
            team_frame,
            image=team_logo,
            bg="#ffffff",
            activebackground="#ac9c7c",
            border=0,
            padx=15,
            pady=15,
            command=lambda abbr=team_abbr: self.toggle_team(abbr)
        )
            
        if not hasattr(self, 'team_logos'):
            self.team_logos = {}

        self.team_logos[team_abbr] = team_logo
        
        team_btn.pack(fill="both", expand=True)
        self.team_buttons[team_abbr] = team_btn
        
        if hasattr(self, '_mousewheel_callbacks'):
            self._bind_mousewheel_to_widget(team_btn)
            self._bind_mousewheel_to_widget(team_frame)


    def toggle_team(self, team_abbr):
        """Toggle team selection."""
        if team_abbr.lower() in self.selected_teams:
            self.selected_teams.remove(team_abbr.lower())
            self.team_buttons[team_abbr].config(bg="#ffffff")

            if hasattr(self.team_buttons[team_abbr], 'cget') and 'text' in str(self.team_buttons[team_abbr].cget('text')):
                self.team_buttons[team_abbr].config(fg="#1a1a2e")
        else:
            self.selected_teams.append(team_abbr.lower())
            self.team_buttons[team_abbr].config(bg="#ac9c7c")

            if hasattr(self.team_buttons[team_abbr], 'cget') and 'text' in str(self.team_buttons[team_abbr].cget('text')):
                self.team_buttons[team_abbr].config(fg="#1a1a2e")
        
        # Show/hide the continue button based on team selection
        if self.selected_teams:
            if not self.continue_btn.winfo_viewable():
                self.continue_btn.pack(side="right", padx=20)
        else:
            if self.continue_btn.winfo_viewable():
                self.continue_btn.pack_forget()


    def show_games(self):
        """Display games for selected teams. You must select at least one team."""
        if not self.selected_teams:
            messagebox.showwarning("No Teams Selected", "Please select at least one team.")
            return
        
        if not self.selected_sport:
            self.show_sport_selection()
            return
        
        sport_mapping = {"nba": "1", "nfl": "2", "mlb": "3"}
        preferences = {
            "sport": sport_mapping[self.selected_sport],
            f"{self.selected_sport}_team": self.selected_teams
        }
        
        self.clear_window()
        
        loading_frame = tk.Frame(self.root, bg="#1a1a2e")
        loading_frame.pack(expand=True, fill="both")
        
        loading_label = tk.Label(
            loading_frame,
            text="Searching for upcoming games...",
            font=("Helvetica", 20),
            fg="#eee2dc",
            bg="#1a1a2e"
        )
        loading_label.pack(expand=True)
        
        self.root.update()
        
        try:          
            file = io.StringIO()
            with contextlib.redirect_stdout(file):
                game_checker(preferences)

            output = file.getvalue()
            self.show_games_result(output)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching games: {str(e)}")
            self.show_team_selection()


    def show_games_result(self, games_output):
        """Display the games result. It will show potential games for today and tomorrow.
        
        Once done, you have the options to go back to the team selection or select a new sport.
        
        Or, you can just close the window.
        """
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both")
        
        header_frame = tk.Frame(main_frame, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(20, 10))
        
        back_btn = tk.Button(
            header_frame,
            text="Back",
            font=("Helvetica", 12),
            bg="#16213e",
            fg="#eee2dc",
            activebackground="#ac9c7c",
            activeforeground="#1a1a2e",
            border=0,
            padx=15,
            pady=5,
            command=self.show_team_selection
        )
        back_btn.pack(side="left", padx=20)
        
        new_search_btn = tk.Button(
            header_frame,
            text="Select New Sport",
            font=("Helvetica", 12),
            bg="#16213e",
            fg="#eee2dc",
            activebackground="#ac9c7c",
            activeforeground="#1a1a2e",
            border=0,
            padx=15,
            pady=5,
            command=self.show_sport_selection
        )
        new_search_btn.pack(side="right", padx=20)
        
        title_label = tk.Label(
            header_frame,
            text="Game Schedule",
            font=("Helvetica", 24, "bold"),
            fg="#eee2dc",
            bg="#1a1a2e"
        )
        title_label.pack()
        
        text_frame = tk.Frame(main_frame, bg="#1a1a2e")
        text_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(
            text_frame,
            bg="#16213e",
            fg="#eee2dc",
            font=("Courier", 11),
            wrap="word",
            padx=15,
            pady=15
        )
        
        scrollbar_text = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar_text.set)
        
        text_widget.insert("1.0", games_output)
        text_widget.config(state="disabled")
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar_text.pack(side="right", fill="y")


    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    app = FridayNightBytesGUI()
    app.run()


if __name__ == "__main__":
    main()