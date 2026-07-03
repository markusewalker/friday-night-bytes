import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamechecker.game_checker import game_checker
from constants import SUPPORTED_LEAGUES
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageOps
import tkinter as tk
import io
import re
import contextlib

class FridayNightBytesGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Friday Night Bytes")
        self.root.geometry("800x600")
        self.root.configure(bg="#16213e")

        self.theme = {
            "bg": "#0b1220",
            "surface": "#111827",
            "surface_alt": "#1f2937",
            "muted": "#94a3b8",
            "text": "#f8fafc",
            "accent": "#f59e0b",
            "accent_soft": "#fbbf24",
            "success": "#34d399",
            "selection": "#ac9c7c"
        }
        
        self.center_window()
        
        self.selected_sport = None
        self.selected_teams = []
        self.team_buttons = {}
        self.team_cards = {}
        
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

        main_frame = tk.Frame(self.root, bg=self.theme["bg"])
        main_frame.pack(expand=True, fill="both")

        content_card = tk.Frame(main_frame, bg=self.theme["surface"], padx=24, pady=24)
        content_card.pack(expand=True, padx=40, pady=40, fill="both")
        
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")

        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((340, 340), Image.Resampling.LANCZOS)
            
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(content_card, image=self.logo_photo, bg=self.theme["surface"])
        logo_label.pack(expand=True, anchor="center")

        self.root.after(5000, self.show_sport_selection)


    def show_sport_selection(self):
        """Display the sport selection screen with clickable sports."""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg=self.theme["bg"])
        main_frame.pack(expand=True, fill="both")

        hero = tk.Frame(main_frame, bg=self.theme["bg"])
        hero.pack(fill="x", pady=(28, 8))

        title_label = tk.Label(
            hero,
            text="Pick Your League",
            font=("Helvetica", 32, "bold"),
            fg=self.theme["text"],
            bg=self.theme["bg"]
        )
        title_label.pack()

        sports_frame = tk.Frame(main_frame, bg=self.theme["bg"])
        sports_frame.pack(expand=True, fill="both", padx=24, pady=20)

        self.create_sport_button(sports_frame, "nba", 0)
        self.create_sport_button(sports_frame, "nfl", 1)
        self.create_sport_button(sports_frame, "mlb", 2)


    def create_sport_button(self, parent, sport_key, row):
        """Create a clickable sport button."""
        sport_frame = tk.Frame(parent, bg=self.theme["surface"], bd=0, highlightthickness=0)
        sport_frame.grid(row=row//3, column=row%3, padx=20, pady=20, sticky="nsew")
        
        parent.grid_rowconfigure(row//3, weight=1)
        parent.grid_columnconfigure(row%3, weight=1)
        
        sport_frame.bind("<Button-1>", lambda e: self.select_sport(sport_key))
        
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", f"{sport_key}-logo.png")
        
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((190, 190), Image.Resampling.LANCZOS)
        sport_logo = ImageTk.PhotoImage(logo_img)
                
        logo_label = tk.Label(
            sport_frame,
            image=sport_logo,
            bg=self.theme["surface"],
            cursor="hand2"
        )
                
        if not hasattr(self, 'sport_logos'):
            self.sport_logos = {}

        self.sport_logos[sport_key] = sport_logo
        
        logo_label.pack(expand=True, pady=(14, 6))
        logo_label.bind("<Button-1>", lambda e: self.select_sport(sport_key))

        sport_name = tk.Label(
            sport_frame,
            text=SUPPORTED_LEAGUES[sport_key]["name"],
            font=("Helvetica", 16, "bold"),
            fg=self.theme["text"],
            bg=self.theme["surface"]
        )
        sport_name.pack(pady=(0, 4))
        sport_name.bind("<Button-1>", lambda e: self.select_sport(sport_key))

        sport_hint = tk.Label(
            sport_frame,
            text="Select and continue",
            font=("Helvetica", 10),
            fg=self.theme["muted"],
            bg=self.theme["surface"]
        )
        sport_hint.pack(pady=(0, 16))
        sport_hint.bind("<Button-1>", lambda e: self.select_sport(sport_key))


        def on_enter(e):
            sport_frame.config(bg=self.theme["surface_alt"], highlightthickness=2, highlightbackground=self.theme["accent_soft"])
            logo_label.config(bg=self.theme["surface_alt"])
            sport_name.config(bg=self.theme["surface_alt"])
            sport_hint.config(bg=self.theme["surface_alt"])


        def on_leave(e):
            sport_frame.config(bg=self.theme["surface"], highlightthickness=0)
            logo_label.config(bg=self.theme["surface"])
            sport_name.config(bg=self.theme["surface"])
            sport_hint.config(bg=self.theme["surface"])
        
        sport_frame.bind("<Enter>", on_enter)
        sport_frame.bind("<Leave>", on_leave)
        logo_label.bind("<Enter>", on_enter)
        logo_label.bind("<Leave>", on_leave)
        sport_name.bind("<Enter>", on_enter)
        sport_name.bind("<Leave>", on_leave)
        sport_hint.bind("<Enter>", on_enter)
        sport_hint.bind("<Leave>", on_leave)
        
        sport_frame.config(width=250, height=320)
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

        main_frame = tk.Frame(self.root, bg=self.theme["bg"])
        main_frame.pack(expand=True, fill="both")

        header_frame = tk.Frame(main_frame, bg=self.theme["bg"])
        header_frame.pack(fill="x", pady=(20, 10))

        back_btn = tk.Button(
            header_frame,
            text="Back",
            font=("Helvetica", 12),
            bg=self.theme["surface"],
            fg=self.theme["text"],
            activebackground=self.theme["accent_soft"],
            activeforeground="#111827",
            border=0,
            padx=15,
            pady=5,
            command=self.show_sport_selection
        )
        back_btn.pack(side="left", padx=20)

        self.continue_btn = tk.Button(
            header_frame,
            text="View Games",
            font=("Helvetica", 12, "bold"),
            bg=self.theme["accent"],
            fg="#111827",
            activebackground=self.theme["accent_soft"],
            activeforeground="#111827",
            border=0,
            padx=15,
            pady=5,
            command=self.show_games
        )
        
        title_label = tk.Label(
            header_frame,
            text=f"{league_info['name']} Teams",
            font=("Helvetica", 24, "bold"),
            fg=self.theme["text"],
            bg=self.theme["bg"],
        )
        title_label.pack(side="left", padx=(34, 0))

        helper_label = tk.Label(
            main_frame,
            text="Choose one or more teams to generate your game board",
            font=("Helvetica", 11),
            fg=self.theme["muted"],
            bg=self.theme["bg"]
        )
        helper_label.pack(anchor="w", padx=24, pady=(0, 10))
        
        canvas = tk.Canvas(main_frame, bg=self.theme["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme["bg"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        teams_wrapper = tk.Frame(scrollable_frame, bg=self.theme["bg"])
        teams_wrapper.pack(expand=True, fill="both", padx=20)
        
        teams_frame = tk.Frame(teams_wrapper, bg=self.theme["bg"])
        teams_frame.pack(fill="both", expand=True, pady=20)
        
        self.team_buttons = {}
        self.team_cards = {}
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
        if not hasattr(self, 'team_cards'):
            self.team_cards = {}

        cols_per_row = getattr(self, 'cols_per_row', 4)
            
        row = index // cols_per_row
        col = index % cols_per_row
        
        team_frame = tk.Frame(parent, bg=self.theme["surface"], relief="flat", bd=0, padx=10, pady=10)
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
        
        logo_size = 88
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        team_logo = ImageTk.PhotoImage(logo_img)
            
        team_btn = tk.Button(
            team_frame,
            image=team_logo,
            bg="#ffffff",
            activebackground=self.theme["selection"],
            border=0,
            padx=15,
            pady=15,
            command=lambda abbr=team_abbr: self.toggle_team(abbr)
        )
            
        if not hasattr(self, 'team_logos'):
            self.team_logos = {}

        self.team_logos[team_abbr] = team_logo
        
        team_btn.pack(fill="both", expand=True)

        team_label = tk.Label(
            team_frame,
            text=team_abbr.upper(),
            font=("Helvetica", 11, "bold"),
            fg=self.theme["text"],
            bg=self.theme["surface"]
        )
        team_label.pack(pady=(10, 2))

        team_name_label = tk.Label(
            team_frame,
            text=team_name,
            font=("Helvetica", 9),
            fg=self.theme["muted"],
            bg=self.theme["surface"],
            wraplength=140,
            justify="center"
        )
        team_name_label.pack(pady=(0, 8))

        status_chip = tk.Label(
            team_frame,
            text="Tap to select",
            font=("Helvetica", 8, "bold"),
            fg=self.theme["muted"],
            bg=self.theme["bg"],
            padx=8,
            pady=3
        )
        status_chip.pack()

        self.team_buttons[team_abbr] = team_btn
        self.team_cards[team_abbr] = {
            "frame": team_frame,
            "label": team_label,
            "name_label": team_name_label,
            "status": status_chip
        }

        def on_card_enter(_event):
            if team_abbr.lower() in self.selected_teams:
                return
            self._apply_team_card_style(team_abbr, selected=False, hovered=True)

        def on_card_leave(_event):
            if team_abbr.lower() in self.selected_teams:
                return
            self._apply_team_card_style(team_abbr, selected=False, hovered=False)

        team_frame.bind("<Enter>", on_card_enter)
        team_frame.bind("<Leave>", on_card_leave)
        team_btn.bind("<Enter>", on_card_enter)
        team_btn.bind("<Leave>", on_card_leave)
        team_label.bind("<Enter>", on_card_enter)
        team_label.bind("<Leave>", on_card_leave)
        team_name_label.bind("<Enter>", on_card_enter)
        team_name_label.bind("<Leave>", on_card_leave)
        status_chip.bind("<Enter>", on_card_enter)
        status_chip.bind("<Leave>", on_card_leave)
        
        if hasattr(self, '_mousewheel_callbacks'):
            self._bind_mousewheel_to_widget(team_btn)
            self._bind_mousewheel_to_widget(team_frame)


    def toggle_team(self, team_abbr):
        """Toggle team selection."""
        card_meta = getattr(self, 'team_cards', {}).get(team_abbr)

        if team_abbr.lower() in self.selected_teams:
            self.selected_teams.remove(team_abbr.lower())
            self.team_buttons[team_abbr].config(bg="#ffffff")
            if card_meta:
                self._apply_team_card_style(team_abbr, selected=False, hovered=False)
        else:
            self.selected_teams.append(team_abbr.lower())
            self.team_buttons[team_abbr].config(bg="#ac9c7c")
            if card_meta:
                self._apply_team_card_style(team_abbr, selected=True, hovered=False)
        
        # Show/hide the continue button based on team selection
        if self.selected_teams:
            if not self.continue_btn.winfo_viewable():
                self.continue_btn.pack(side="right", padx=20)
        else:
            if self.continue_btn.winfo_viewable():
                self.continue_btn.pack_forget()


    def _apply_team_card_style(self, team_abbr, selected, hovered):
        """Apply visual state to a team card based on selected/hovered status."""
        card_meta = getattr(self, 'team_cards', {}).get(team_abbr)
        if not card_meta:
            return

        frame_bg = self.theme["surface_alt"] if (selected or hovered) else self.theme["surface"]
        label_fg = self.theme["accent_soft"] if selected else self.theme["text"]
        name_fg = self.theme["text"] if selected else self.theme["muted"]
        status_text = "Selected" if selected else "Tap to select"
        status_fg = "#111827" if selected else self.theme["muted"]
        status_bg = self.theme["accent_soft"] if selected else self.theme["bg"]

        card_meta["frame"].config(
            bg=frame_bg,
            highlightthickness=2 if (selected or hovered) else 0,
            highlightbackground=self.theme["accent"] if selected else self.theme["accent_soft"]
        )
        card_meta["label"].config(bg=frame_bg, fg=label_fg)
        card_meta["name_label"].config(bg=frame_bg, fg=name_fg)
        card_meta["status"].config(text=status_text, fg=status_fg, bg=status_bg)


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

        loading_frame = tk.Frame(self.root, bg=self.theme["bg"])
        loading_frame.pack(expand=True, fill="both")

        loading_card = tk.Frame(loading_frame, bg=self.theme["surface"], padx=30, pady=30)
        loading_card.pack(expand=True, padx=40, pady=40)

        loading_label = tk.Label(
            loading_card,
            text="Searching for upcoming games...",
            font=("Helvetica", 22, "bold"),
            fg=self.theme["text"],
            bg=self.theme["surface"]
        )

        loading_label.pack(pady=(0, 10))
  
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

        # Rich color palette for a more modern-looking results experience.
        page_bg = "#0f172a"
        card_bg = "#111827"
        accent = "#f59e0b"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        success = "#34d399"

        game_cards = self._extract_game_cards(games_output)

        main_frame = tk.Frame(self.root, bg=page_bg)
        main_frame.pack(expand=True, fill="both")

        header_frame = tk.Frame(main_frame, bg=page_bg)
        header_frame.pack(fill="x", pady=(20, 10))

        back_btn = tk.Button(
            header_frame,
            text="Back",
            font=("Helvetica", 12),
            bg=card_bg,
            fg=text_primary,
            activebackground=accent,
            activeforeground="#111827",
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
            bg=card_bg,
            fg=text_primary,
            activebackground=accent,
            activeforeground="#111827",
            border=0,
            padx=15,
            pady=5,
            command=self.show_sport_selection
        )
        new_search_btn.pack(side="right", padx=20)

        title_label = tk.Label(
            header_frame,
            text="Your Game Night Board",
            font=("Helvetica", 24, "bold"),
            fg=text_primary,
            bg=page_bg
        )
        title_label.pack()

        stats_frame = tk.Frame(main_frame, bg=page_bg)
        stats_frame.pack(fill="x", padx=20)

        self._create_stat_chip(stats_frame, "Sport", str(self.selected_sport).upper() if self.selected_sport else "N/A", card_bg, text_primary, text_secondary)
        self._create_stat_chip(stats_frame, "Teams", str(len(self.selected_teams)), card_bg, text_primary, text_secondary)
        self._create_stat_chip(stats_frame, "Games Found", str(len(game_cards)), card_bg, success, text_secondary)

        content_frame = tk.Frame(main_frame, bg=page_bg)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(15, 20))

        cards_frame = tk.Frame(content_frame, bg=page_bg)
        cards_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        cards_canvas = tk.Canvas(cards_frame, bg=page_bg, highlightthickness=0)
        cards_scrollbar = ttk.Scrollbar(cards_frame, orient="vertical", command=cards_canvas.yview)
        cards_container = tk.Frame(cards_canvas, bg=page_bg)

        cards_container.bind(
            "<Configure>",
            lambda e: cards_canvas.configure(scrollregion=cards_canvas.bbox("all"))
        )

        cards_canvas.create_window((0, 0), window=cards_container, anchor="nw")
        cards_canvas.configure(yscrollcommand=cards_scrollbar.set)

        if game_cards:
            for card in game_cards:
                self._create_game_card(cards_container, card, card_bg, text_primary, text_secondary, accent)
        else:
            empty_card = tk.Frame(cards_container, bg=card_bg, padx=20, pady=20)
            empty_card.pack(fill="x", pady=(0, 12))

            empty_title = tk.Label(
                empty_card,
                text="No games found this week",
                font=("Helvetica", 16, "bold"),
                fg=text_primary,
                bg=card_bg
            )
            empty_title.pack(anchor="w")

            empty_body = tk.Label(
                empty_card,
                text="Try selecting different teams or check back tomorrow for new schedules.",
                font=("Helvetica", 10),
                fg=text_secondary,
                bg=card_bg,
                justify="left"
            )
            empty_body.pack(anchor="w", pady=(8, 0))

        cards_canvas.pack(side="left", fill="both", expand=True)
        cards_scrollbar.pack(side="right", fill="y")


    def _create_stat_chip(self, parent, label, value, bg, value_color, label_color):
        """Create compact stat chips used in the results header."""
        chip = tk.Frame(parent, bg=bg, padx=12, pady=10)
        chip.pack(side="left", padx=(0, 12), pady=(0, 4))

        chip_value = tk.Label(
            chip,
            text=value,
            font=("Helvetica", 14, "bold"),
            fg=value_color,
            bg=bg
        )
        chip_value.pack(anchor="w")

        chip_label = tk.Label(
            chip,
            text=label,
            font=("Helvetica", 9),
            fg=label_color,
            bg=bg
        )
        chip_label.pack(anchor="w")


    def _create_game_card(self, parent, card, bg, title_fg, body_fg, accent):
        """Render one game card with matchup and schedule details."""
        wrapper = tk.Frame(parent, bg=bg, padx=16, pady=16)
        wrapper.pack(fill="x", pady=(0, 12))

        centered = tk.Frame(wrapper, bg=bg)
        centered.pack(anchor="center")

        logos_row = tk.Frame(centered, bg=bg)
        logos_row.pack(anchor="center")

        left_logo = self._get_result_team_logo(card.get("team_abbr"), card.get("team"), 52)
        right_logo = self._get_result_team_logo(card.get("opponent_abbr"), card.get("opponent"), 52)

        left_logo_label = tk.Label(logos_row, image=left_logo, bg=bg)
        left_logo_label.image = left_logo
        left_logo_label.grid(row=0, column=0, padx=(4, 12))

        versus = tk.Label(
            logos_row,
            text="VS",
            font=("Helvetica", 11, "bold"),
            fg=accent,
            bg=bg
        )
        versus.grid(row=0, column=1)

        right_logo_label = tk.Label(logos_row, image=right_logo, bg=bg)
        right_logo_label.image = right_logo
        right_logo_label.grid(row=0, column=2, padx=(12, 4))

        matchup_label = tk.Label(
            centered,
            text=card["matchup"],
            font=("Helvetica", 15, "bold"),
            fg=title_fg,
            bg=bg,
            justify="center"
        )
        matchup_label.pack(anchor="center", pady=(12, 0))

        meta_text = f"{card['when']}"
        meta_label = tk.Label(
            centered,
            text=meta_text,
            font=("Helvetica", 10),
            fg=body_fg,
            bg=bg,
            justify="center"
        )
        meta_label.pack(anchor="center", pady=(6, 0))

        badges = tk.Frame(centered, bg=bg)
        badges.pack(anchor="center", pady=(10, 0))

        venue_label = tk.Label(
            badges,
            text=card["venue_label"],
            font=("Helvetica", 9, "bold"),
            fg="#111827",
            bg=accent,
            padx=8,
            pady=4
        )
        venue_label.pack(side="left", padx=(0, 8))

        team_chip = tk.Label(
            badges,
            text=card.get("team_abbr", ""),
            font=("Helvetica", 9, "bold"),
            fg=title_fg,
            bg="#1f2937",
            padx=8,
            pady=4
        )
        team_chip.pack(side="left")


    def _extract_game_cards(self, games_output):
        """Parse printed game table rows into structured cards for the UI."""
        cards = []

        for raw_line in games_output.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            # Skip separators and known non-data rows from terminal output.
            if line.startswith("─") or line.startswith("Games for your favorite teams"):
                continue
            if line.startswith("Team") and "Matchup" in line and "Date/Time" in line:
                continue

            parts = re.split(r"\s{2,}", line)
            if len(parts) < 3:
                continue

            team, matchup, venue_and_time = parts[0], parts[1], parts[2]
            if " vs " not in matchup and " @ " not in matchup:
                continue
            if not venue_and_time:
                continue

            venue = venue_and_time[0]
            when = venue_and_time[1:].strip() if len(venue_and_time) > 1 else "TBD"
            venue_label = "Home Game" if venue == "🏠" else "Away Game"

            opponent = "Unknown"
            if " vs " in matchup:
                opponent = matchup.split(" vs ", 1)[1].strip()
            elif " @ " in matchup:
                opponent = matchup.split(" @ ", 1)[1].strip()

            team_abbr = self._get_team_abbreviation_from_name(team)
            opponent_abbr = self._get_team_abbreviation_from_name(opponent)

            cards.append({
                "team": team,
                "matchup": matchup,
                "opponent": opponent,
                "team_abbr": team_abbr,
                "opponent_abbr": opponent_abbr,
                "when": when or "TBD",
                "venue_label": venue_label
            })

        return cards


    def _get_team_abbreviation_from_name(self, team_name):
        """Get team abbreviation from full team name for the selected sport."""
        if not team_name or not self.selected_sport or self.selected_sport not in SUPPORTED_LEAGUES:
            return ""

        for full_name, abbr in SUPPORTED_LEAGUES[self.selected_sport]["teams"]:
            if full_name.lower() == team_name.lower():
                return abbr.upper()

        return ""


    def _get_result_team_logo(self, team_abbr, team_name, size):
        """Load and cache a team logo used in game result cards."""
        if not hasattr(self, "result_logos"):
            self.result_logos = {}

        cache_key = f"{self.selected_sport}:{team_abbr}:{team_name}:{size}"
        if cache_key in self.result_logos:
            return self.result_logos[cache_key]

        base_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "teamlogos",
            str(self.selected_sport)
        )

        candidates = []
        if team_abbr:
            candidates.append(f"{team_abbr.lower()}.png")
        if team_name:
            candidates.append(f"{team_name.lower().replace(' ', '_')}.png")

        logo_path = None
        for filename in candidates:
            potential = os.path.join(base_dir, filename)
            if os.path.exists(potential):
                logo_path = potential
                break

        if logo_path:
            logo_img = Image.open(logo_path).convert("RGBA")
        else:
            logo_img = Image.new("RGBA", (size, size), (31, 41, 55, 255))

        badge = self._build_logo_badge(logo_img, size)
        logo_photo = ImageTk.PhotoImage(badge)
        self.result_logos[cache_key] = logo_photo
        return logo_photo


    def _build_logo_badge(self, logo_img, size):
        """Create a circular logo badge with a subtle glow and rim."""
        rim_color = (251, 191, 36, 255)
        glow_color = (245, 158, 11, 76)
        plate_color = (31, 41, 55, 255)
        badge_size = size

        badge = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(badge)

        draw.ellipse((1, 1, badge_size - 2, badge_size - 2), fill=glow_color)
        draw.ellipse((4, 4, badge_size - 5, badge_size - 5), fill=plate_color, outline=rim_color, width=2)

        inner_size = max(12, badge_size - 12)
        fitted_logo = ImageOps.fit(logo_img, (inner_size, inner_size), method=Image.Resampling.LANCZOS)

        mask = Image.new("L", (inner_size, inner_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, inner_size - 1, inner_size - 1), fill=255)

        offset = ((badge_size - inner_size) // 2, (badge_size - inner_size) // 2)
        badge.paste(fitted_logo, offset, mask)
        return badge


    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    app = FridayNightBytesGUI()
    app.run()


if __name__ == "__main__":
    main()