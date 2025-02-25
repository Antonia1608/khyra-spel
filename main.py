import tkinter as tk
from tkinter import ttk
import random
from game_data import DOG_GAMES
import os
from PIL import Image, ImageTk
import json
from datetime import datetime

class DogGameGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Speel mee met Khyra")
        self.root.resizable(True, True)
        self.root.geometry("900x700")
        self.root.configure(bg='#fae8e6')

        if os.path.exists("dog_icon.ico"):
            self.root.iconbitmap("dog_icon.ico")
        
        # Create a canvas with scrollbars
        self.canvas = tk.Canvas(root, bg='#fae8e6')
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        
        # Configure root grid
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # Place canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create main frame inside canvas
        main_frame = ttk.Frame(self.canvas, padding="30")
        
        # Add main_frame to canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=main_frame, anchor="nw")
        
        # Configure main_frame events
        main_frame.bind("<Configure>", self._configure_main_frame)
        self.canvas.bind("<Configure>", self._configure_canvas)
        
        # Style configuratie
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Book Antiqua', 28, 'bold'), foreground='#c82848')
        style.configure('Game.TLabel', font=('Book Antiqua', 11), foreground='#c82848')
        style.configure('Header.TLabel', font=('Book Antiqua', 18, 'bold'), foreground='#c82848')
        style.configure('Tip.TLabel', font=('Book Antiqua', 10, 'italic'), foreground='#c82848')
        
        # Basis frame styling
        style.configure('TFrame', background='#fae8e6')
        
        # Custom frame styling voor kaders
        style.configure('CustomFrame.TLabelframe', 
                       background='#d7cb59',
                       borderwidth=4,
                       relief="solid")
        style.configure('CustomFrame.TLabelframe.Label', 
                       background='#d7cb59',
                       foreground='#c82848',
                       font=('Book Antiqua', 12, 'bold'))
        
        # Titel en foto frame
        title_frame = ttk.Frame(main_frame, style='TFrame')
        title_frame.grid(row=0, column=0, pady=20)
        title_frame.grid_columnconfigure(1, weight=1)
        
        # Laad en verwerk de foto van Khyra
        try:
            image = Image.open("khrya.jpg")
            width, height = image.size
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
            image = image.crop((left, top, right, bottom))
            image = image.resize((250, 250), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            photo_label = ttk.Label(title_frame, image=self.photo, background='#fae8e6')
            photo_label.grid(row=0, column=0, padx=10)
        except Exception as e:
            print(f"Kon foto niet laden: {e}")
            photo_label = ttk.Label(title_frame, text="[Foto]", background='#fae8e6')
            photo_label.grid(row=0, column=0, padx=10)
        
        # Titel naast de foto
        title_label = ttk.Label(title_frame, 
                              text="Speel mee met Khyra",
                              style='Title.TLabel',
                              background='#fae8e6')
        title_label.grid(row=0, column=1, padx=10, sticky='EW')
        
        # Knop met opmaak
        self.generate_button = tk.Button(main_frame, 
                                       text="Nieuw Spelletje!",
                                       font=('Book Antiqua', 16, 'bold'),
                                       bg='#15babc',
                                       fg='#ffffff',
                                       relief='raised',
                                       command=self.generate_game,
                                       padx=20,
                                       pady=10,
                                       cursor='hand2')
        self.generate_button.grid(row=0, column=0, pady=(150,0), padx=(350,75))
        
        # Game frame met custom style
        self.game_frame = ttk.LabelFrame(main_frame, 
                                       text="✨ Jouw spelletje ✨", 
                                       padding="20",
                                       style='CustomFrame.TLabelframe')
        self.game_frame.grid(row=2, column=0, pady=15, sticky=(tk.W, tk.E))
        
        # Labels voor speldetails binnen game frame
        self.name_label = ttk.Label(self.game_frame, text="", 
                                  style='Header.TLabel',
                                  background='#d7cb59')
        self.name_label.grid(row=0, column=0, pady=5, sticky=tk.W)
        
        self.desc_label = ttk.Label(self.game_frame, text="", 
                                  wraplength=625,
                                  style='Game.TLabel',
                                  background='#d7cb59')
        self.desc_label.grid(row=1, column=0, pady=5, sticky=tk.W)
        
        self.details_label = ttk.Label(self.game_frame, text="", 
                                     style='Game.TLabel',
                                     background='#d7cb59')
        self.details_label.grid(row=2, column=0, pady=5, sticky=tk.W)
        
        # Filter frame met custom style
        filter_frame = ttk.LabelFrame(main_frame, 
                                    text="🎯 Kies je spelletje", 
                                    padding="20",
                                    style='CustomFrame.TLabelframe')
        filter_frame.grid(row=3, column=0, pady=(15,30), sticky=(tk.W, tk.E))
        
        # Grid configuratie voor filter frame
        filter_frame.grid_columnconfigure(1, weight=1)
        filter_frame.grid_columnconfigure(3, weight=1)
        
        # Labels en comboboxes binnen filter frame
        ttk.Label(filter_frame, text="Moeilijkheid:", 
                 style='Game.TLabel',
                 background='#d7cb59').grid(row=0, column=0, padx=5)
        
        self.difficulty_var = tk.StringVar(value="Alle")
        difficulty_combo = ttk.Combobox(filter_frame, 
                                      textvariable=self.difficulty_var,
                                      values=["Alle", "Makkelijk", "Gemiddeld", "Moeilijk", "Extra uitdagend"],
                                      font=('Book Antiqua', 10))
        difficulty_combo.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(filter_frame, text="Max. Duur:", 
                 style='Game.TLabel',
                 background='#d7cb59').grid(row=0, column=2, padx=5)
        
        self.max_duration_var = tk.StringVar(value="Alle")
        duration_combo = ttk.Combobox(filter_frame, 
                                    textvariable=self.max_duration_var,
                                    values=["Alle", "5 min", "10 min", "15 min", "20 min"],
                                    font=('Book Antiqua', 10))
        duration_combo.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(filter_frame, text="Type:", 
                 style='Game.TLabel',
                 background='#d7cb59').grid(row=1, column=0, padx=5, pady=(10,0))
        
        self.type_var = tk.StringVar(value="Alle")
        type_combo = ttk.Combobox(filter_frame, 
                                textvariable=self.type_var,
                                values=["Alle", "Herstel", "Actief", "Mentaal"],
                                font=('Book Antiqua', 10))
        type_combo.grid(row=1, column=1, padx=5, pady=(10,0), sticky=(tk.W, tk.E))
        
        # Tip label
        self.tip_label = ttk.Label(main_frame, 
                                text="💡 Tip: Kies 'Herstel' voor rustige spelletjes tijdens herstel",
                                style='Tip.TLabel',
                                wraplength=625,
                                background='#fae8e6')
        self.tip_label.grid(row=4, column=0, pady=(15,40))

        # History button
        self.history_button = tk.Button(main_frame,
                                      text="Bekijk Geschiedenis",
                                      font=('Book Antiqua', 12),
                                      bg='#15babc',
                                      fg='#ffffff',
                                      command=self.show_history)
        self.history_button.grid(row=5, column=0, pady=10, sticky='E')

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
        history_window.configure(bg='#fae8e6')
        
        # Create a frame for the history
        history_frame = ttk.Frame(history_window, style='TFrame')
        history_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Add a title
        title_label = ttk.Label(history_frame,
                              text="Gespeelde Spelletjes",
                              style='Title.TLabel',
                              background='#fae8e6')
        title_label.pack(pady=10)
        
        try:
            with open('game_history.json', 'r') as f:
                history = json.load(f)
            
            # Create scrollable frame for history items
            canvas = tk.Canvas(history_frame, bg='#fae8e6')
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
                                     background='#fae8e6')
                game_label.pack(side='left')
                
                date_label = ttk.Label(game_frame,
                                     text=item['played_at'],
                                     style='Tip.TLabel',
                                     background='#fae8e6')
                date_label.pack(side='right')
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except FileNotFoundError:
            empty_label = ttk.Label(history_frame,
                                  text="Nog geen spelletjes gespeeld",
                                  style='Game.TLabel',
                                  background='#fae8e6')
            empty_label.pack(pady=20)
            
    def _configure_main_frame(self, event):
        """Reset the scroll region to encompass the inner frame"""
        size = (event.width, event.height)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _configure_canvas(self, event):
        """Update the inner frame's width to fill the canvas"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def generate_game(self):
        self.game_frame.grid_remove()
        self.root.update()
        
        filtered_games = DOG_GAMES.copy()
        
        if self.difficulty_var.get() != "Alle":
            filtered_games = [game for game in filtered_games 
                            if game["difficulty"] == self.difficulty_var.get()]
        
        if self.max_duration_var.get() != "Alle":
            max_minutes = int(self.max_duration_var.get().split()[0])
            filtered_games = [game for game in filtered_games 
                            if int(game["duration"].split()[0].split("-")[0]) <= max_minutes]
        
        if self.type_var.get() != "Alle":
            filtered_games = [game for game in filtered_games 
                            if game["type"] == self.type_var.get()]
        
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
            self.save_game_to_history(game)
        
        self.game_frame.grid()

def main():
    root = tk.Tk()
    app = DogGameGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()