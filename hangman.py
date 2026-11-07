import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("600x550")
        self.root.configure(bg="#2c3e50")
        
        # Word list with categories - Primary School Syllabus
        self.word_categories = {
            # English/Language
            "ADJECTIVE": "Grammar",
            "NOUN": "Grammar",
            "VERB": "Grammar",
            "SENTENCE": "Writing",
            "PARAGRAPH": "Writing",
            "STORY": "Literature",
            "POEM": "Literature",
            "DICTIONARY": "Reference",
            "ALPHABET": "Language",
            "VOWEL": "Phonics",
            "CONSONANT": "Phonics",
            "SYLLABLE": "Phonics",
            "RHYME": "Poetry",
            "COMPREHENSION": "Reading",
            
            # Mathematics
            "ADDITION": "Math",
            "SUBTRACTION": "Math",
            "MULTIPLICATION": "Math",
            "DIVISION": "Math",
            "FRACTION": "Math",
            "DECIMAL": "Math",
            "PERCENTAGE": "Math",
            "GEOMETRY": "Math",
            "TRIANGLE": "Shapes",
            "CIRCLE": "Shapes",
            "SQUARE": "Shapes",
            "RECTANGLE": "Shapes",
            "MEASUREMENT": "Math",
            "CALCULATOR": "Tools",
            "EQUATION": "Math",
            "GRAPH": "Math",
            
            # Science
            "PLANT": "Biology",
            "ANIMAL": "Biology",
            "HABITAT": "Ecology",
            "ECOSYSTEM": "Ecology",
            "PHOTOSYNTHESIS": "Biology",
            "OXYGEN": "Chemistry",
            "CARBON": "Chemistry",
            "WATER": "Matter",
            "ENERGY": "Physics",
            "GRAVITY": "Physics",
            "MAGNET": "Physics",
            "ELECTRICITY": "Physics",
            "WEATHER": "Earth Science",
            "SEASONS": "Earth Science",
            "VOLCANO": "Geology",
            "EARTHQUAKE": "Geology",
            "FOSSIL": "Paleontology",
            "EVOLUTION": "Biology",
            "CELL": "Biology",
            "MICROSCOPE": "Science Tools",
            
            # Geography/Social Studies
            "CONTINENT": "Geography",
            "OCEAN": "Geography",
            "MOUNTAIN": "Landforms",
            "RIVER": "Geography",
            "DESERT": "Landforms",
            "FOREST": "Geography",
            "ISLAND": "Geography",
            "COUNTRY": "Geography",
            "CAPITAL": "Geography",
            "MAP": "Geography",
            "COMPASS": "Navigation",
            "COMMUNITY": "Social Studies",
            "GOVERNMENT": "Civics",
            "DEMOCRACY": "Government",
            "CITIZEN": "Civics",
            "HISTORY": "Social Studies",
            "CULTURE": "Social Studies",
            "TRADITION": "Culture",
            
            # Health/Physical Education
            "EXERCISE": "Health",
            "NUTRITION": "Health",
            "VITAMIN": "Health",
            "MUSCLE": "Anatomy",
            "SKELETON": "Anatomy",
            "HEART": "Anatomy",
            "BRAIN": "Anatomy",
            "LUNGS": "Anatomy",
            "HYGIENE": "Health",
            "SAFETY": "Health",
            
            # Art/Music
            "PAINTING": "Art",
            "DRAWING": "Art",
            "SCULPTURE": "Art",
            "COLOR": "Art",
            "MUSIC": "Performing Arts",
            "RHYTHM": "Music",
            "MELODY": "Music",
            "INSTRUMENT": "Music",
            "DANCE": "Performing Arts",
            "THEATER": "Performing Arts",
            
            # General
            "LIBRARY": "School",
            "CLASSROOM": "School",
            "TEACHER": "School",
            "STUDENT": "School",
            "PRINCIPAL": "School",
            "HOMEWORK": "School",
            "EXAM": "School",
            "PROJECT": "School",
            "FRIENDSHIP": "Values",
            "RESPECT": "Values",
            "RESPONSIBILITY": "Values",
            "COOPERATION": "Values"
        }
        
        # Game state
        self.secret_word = ""
        self.secret_category = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6
        self.game_over = False
        self.clue_shown = False
        
        # Create UI
        self.create_widgets()
        self.new_game()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="HANGMAN", 
            font=("Arial", 28, "bold"),
            bg="#2c3e50", 
            fg="#ecf0f1"
        )
        title_label.pack(pady=10)
        
        # Canvas for hangman drawing
        self.canvas = tk.Canvas(
            self.root, 
            width=200, 
            height=200, 
            bg="#34495e",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Word display
        self.word_label = tk.Label(
            self.root, 
            text="", 
            font=("Courier", 24, "bold"),
            bg="#2c3e50", 
            fg="#ecf0f1"
        )
        self.word_label.pack(pady=10)
        
        # Wrong guesses display
        self.wrong_label = tk.Label(
            self.root, 
            text="Wrong guesses: 0/6", 
            font=("Arial", 12),
            bg="#2c3e50", 
            fg="#e74c3c"
        )
        self.wrong_label.pack(pady=5)
        
        # Used letters display
        self.used_label = tk.Label(
            self.root, 
            text="Used letters: ", 
            font=("Arial", 10),
            bg="#2c3e50", 
            fg="#95a5a6"
        )
        self.used_label.pack(pady=5)
        
        # Clue display
        self.clue_label = tk.Label(
            self.root, 
            text="Category: ???", 
            font=("Arial", 11, "bold"),
            bg="#2c3e50", 
            fg="#f39c12"
        )
        self.clue_label.pack(pady=5)
        
        # Keyboard frame
        self.keyboard_frame = tk.Frame(self.root, bg="#2c3e50")
        self.keyboard_frame.pack(pady=10)
        
        # Create letter buttons
        self.letter_buttons = {}
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(letters):
            row = i // 9
            col = i % 9
            btn = tk.Button(
                self.keyboard_frame,
                text=letter,
                font=("Arial", 10, "bold"),
                width=3,
                height=1,
                bg="#3498db",
                fg="white",
                activebackground="#2980b9",
                activeforeground="white",
                relief="flat",
                command=lambda l=letter: self.guess_letter(l)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.letter_buttons[letter] = btn
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#2c3e50")
        buttons_frame.pack(pady=10)
        
        # Clue button
        clue_btn = tk.Button(
            buttons_frame,
            text="Show Clue",
            font=("Arial", 12, "bold"),
            bg="#f39c12",
            fg="white",
            activebackground="#e67e22",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=self.show_clue
        )
        clue_btn.pack(side="left", padx=10)
        
        # New game button
        new_game_btn = tk.Button(
            buttons_frame,
            text="New Game",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=self.new_game
        )
        new_game_btn.pack(side="left", padx=10)
    
    def new_game(self):
        # Reset game state
        self.secret_word = random.choice(list(self.word_categories.keys()))
        self.secret_category = self.word_categories[self.secret_word]
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.game_over = False
        self.clue_shown = False
        
        # Reset letter buttons
        for letter, btn in self.letter_buttons.items():
            btn.config(state="normal", bg="#3498db")
        
        # Clear canvas and draw gallows
        self.canvas.delete("all")
        self.draw_gallows()
        
        # Reset clue display
        self.clue_label.config(text="Category: ???")
        
        # Update displays
        self.update_display()
    
    def draw_gallows(self):
        # Draw gallows
        self.canvas.create_line(20, 180, 100, 180, width=3, fill="#ecf0f1")  # Base
        self.canvas.create_line(60, 180, 60, 20, width=3, fill="#ecf0f1")    # Pole
        self.canvas.create_line(60, 20, 120, 20, width=3, fill="#ecf0f1")     # Top
        self.canvas.create_line(120, 20, 120, 40, width=3, fill="#ecf0f1")   # Rope
    
    def draw_hangman(self):
        # Draw body parts based on wrong guesses
        if self.wrong_guesses >= 1:  # Head
            self.canvas.create_oval(105, 40, 135, 70, width=3, outline="#ecf0f1")
        if self.wrong_guesses >= 2:  # Body
            self.canvas.create_line(120, 70, 120, 120, width=3, fill="#ecf0f1")
        if self.wrong_guesses >= 3:  # Left arm
            self.canvas.create_line(120, 80, 90, 100, width=3, fill="#ecf0f1")
        if self.wrong_guesses >= 4:  # Right arm
            self.canvas.create_line(120, 80, 150, 100, width=3, fill="#ecf0f1")
        if self.wrong_guesses >= 5:  # Left leg
            self.canvas.create_line(120, 120, 90, 150, width=3, fill="#ecf0f1")
        if self.wrong_guesses >= 6:  # Right leg
            self.canvas.create_line(120, 120, 150, 150, width=3, fill="#ecf0f1")
    
    def guess_letter(self, letter):
        if self.game_over or letter in self.guessed_letters:
            return
        
        self.guessed_letters.add(letter)
        self.letter_buttons[letter].config(state="disabled")
        
        if letter not in self.secret_word:
            self.wrong_guesses += 1
            self.letter_buttons[letter].config(bg="#e74c3c")
            self.draw_hangman()
        else:
            self.letter_buttons[letter].config(bg="#27ae60")
        
        self.update_display()
        self.check_game_over()
    
    def update_display(self):
        # Update word display
        display_word = ""
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        self.word_label.config(text=display_word.strip())
        
        # Update wrong guesses
        self.wrong_label.config(text=f"Wrong guesses: {self.wrong_guesses}/{self.max_wrong_guesses}")
        
        # Update used letters
        used_letters = " ".join(sorted(self.guessed_letters))
        self.used_label.config(text=f"Used letters: {used_letters}")
    
    def show_clue(self):
        if not self.clue_shown and not self.game_over:
            self.clue_shown = True
            self.clue_label.config(text=f"Category: {self.secret_category}")
    
    def check_game_over(self):
        # Check if player won
        if all(letter in self.guessed_letters for letter in self.secret_word):
            self.game_over = True
            messagebox.showinfo("Congratulations!", f"You won! The word was: {self.secret_word}")
            return
        
        # Check if player lost
        if self.wrong_guesses >= self.max_wrong_guesses:
            self.game_over = True
            messagebox.showinfo("Game Over", f"You lost! The word was: {self.secret_word}")
            return

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
