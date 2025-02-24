[Previous main.py content with added imports and new functions:

import json
from datetime import datetime

# Add to __init__:
        # History button
        self.history_button = tk.Button(main_frame,
                                      text="Bekijk Geschiedenis",
                                      font=('Book Antiqua', 12),
                                      bg='#15babc',
                                      fg='#ffffff',
                                      command=self.show_history)
        self.history_button.grid(row=5, column=0, pady=10, sticky='E')

# New functions:
    def save_game_to_history(self, game):
        try:
            with open('game_history.json', 'r') as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []
        
        game_entry = {
            "name": game["name"],
            "type": game["type"],
            "difficulty": game["difficulty"],
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        history.append(game_entry)
        
        with open('game_history.json', 'w') as f:
            json.dump(history, f, indent=4)

    def show_history(self):
        # Create a new window for history
        history_window = tk.Toplevel(self.root)
        history_window.title("Spelgeschiedenis")
        history_window.geometry("600x400")
        history_window.configure(bg='#fdcfca')
        
        # Create a frame for the history
        history_frame = ttk.Frame(history_window, style='TFrame')
        history_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Add a title
        title_label = ttk.Label(history_frame,
                              text="Gespeelde Spelletjes",
                              style='Title.TLabel',
                              background='#fdcfca')
        title_label.pack(pady=10)
        
        try:
            with open('game_history.json', 'r') as f:
                history = json.load(f)
            
            # Create scrollable frame for history items
            canvas = tk.Canvas(history_frame, bg='#fdcfca')
            scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add history items
            for item in reversed(history):
                game_frame = ttk.Frame(scrollable_frame, style='TFrame')
                game_frame.pack(fill='x', pady=5)
                
                game_label = ttk.Label(game_frame,
                                     text=f"{item['name']} ({item['type']})",
                                     style='Game.TLabel',
                                     background='#fdcfca')
                game_label.pack(side='left')
                
                date_label = ttk.Label(game_frame,
                                     text=item['played_at'],
                                     style='Tip.TLabel',
                                     background='#fdcfca')
                date_label.pack(side='right')
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except FileNotFoundError:
            empty_label = ttk.Label(history_frame,
                                  text="Nog geen spelletjes gespeeld",
                                  style='Game.TLabel',
                                  background='#fdcfca')
            empty_label.pack(pady=20)

# Modify generate_game to save history:
        if not filtered_games:
            self.name_label.config(text="🤔 Geen spelletjes gevonden met deze criteria!")
            self.desc_label.config(text="")
            self.details_label.config(text="")
        else:
            game = random.choice(filtered_games)
            self.name_label.config(text=f"🎯 {game['name']}")
            self.desc_label.config(text=f"📝 {game['description']}")
            self.details_label.config(
                text=f"\n⏱️ Duur: {game['duration']}\n📊 Moeilijkheid: {game['difficulty']}\n🎮 Type: {game['type']}")
            # Save to history
            self.save_game_to_history(game)]