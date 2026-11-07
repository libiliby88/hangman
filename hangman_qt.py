"""Hangman game with PyQt6 (alternate UI to hangman.py)."""

from __future__ import annotations

import random
import sys

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

MAX_WRONG_GUESSES = 6
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

BACKGROUND = "#2c3e50"
CANVAS_BACKGROUND = "#34495e"
FOREGROUND = "#ecf0f1"

# Word list with categories - Primary School Syllabus
WORD_CATEGORIES = {
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
    "COOPERATION": "Values",
}


class GallowsCanvas(QWidget):
    """Draws the gallows and one body part per wrong guess."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self._wrong_guesses = 0

    def set_wrong_guesses(self, count: int) -> None:
        self._wrong_guesses = count
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(CANVAS_BACKGROUND))
        painter.setPen(QPen(QColor(FOREGROUND), 3))

        painter.drawLine(20, 180, 100, 180)  # Base
        painter.drawLine(60, 180, 60, 20)  # Pole
        painter.drawLine(60, 20, 120, 20)  # Top
        painter.drawLine(120, 20, 120, 40)  # Rope

        if self._wrong_guesses >= 1:  # Head
            painter.drawEllipse(QPointF(120, 55), 15, 15)
        if self._wrong_guesses >= 2:  # Body
            painter.drawLine(120, 70, 120, 120)
        if self._wrong_guesses >= 3:  # Left arm
            painter.drawLine(120, 80, 90, 100)
        if self._wrong_guesses >= 4:  # Right arm
            painter.drawLine(120, 80, 150, 100)
        if self._wrong_guesses >= 5:  # Left leg
            painter.drawLine(120, 120, 90, 150)
        if self._wrong_guesses >= 6:  # Right leg
            painter.drawLine(120, 120, 150, 150)


def _letter_style(background: str) -> str:
    return (
        "QPushButton {"
        f"background-color: {background};"
        "color: white;"
        "border: none;"
        "border-radius: 4px;"
        "font: bold 10pt 'Arial';"
        "}"
        "QPushButton:hover { background-color: #2980b9; }"
        "QPushButton:disabled { color: #ecf0f1; }"
    )


def _action_style(background: str, hover: str) -> str:
    return (
        "QPushButton {"
        f"background-color: {background};"
        "color: white;"
        "border: none;"
        "border-radius: 4px;"
        "padding: 6px 20px;"
        "font: bold 12pt 'Arial';"
        "}"
        f"QPushButton:hover {{ background-color: {hover}; }}"
    )


class HangmanWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Hangman Game (PyQt6)")
        self.resize(600, 620)
        self.setStyleSheet(f"QMainWindow {{ background-color: {BACKGROUND}; }}")

        self.secret_word = ""
        self.secret_category = ""
        self.guessed_letters: set[str] = set()
        self.wrong_guesses = 0
        self.game_over = False
        self.clue_shown = False

        self._create_widgets()
        self.new_game()

    def _create_widgets(self) -> None:
        central = QWidget()
        central.setStyleSheet(f"background-color: {BACKGROUND}; color: {FOREGROUND};")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 10, 16, 16)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title = QLabel("HANGMAN")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.canvas = GallowsCanvas()
        layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.word_label = QLabel("")
        self.word_label.setFont(QFont("Courier", 24, QFont.Weight.Bold))
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.word_label)

        self.wrong_label = QLabel(f"Wrong guesses: 0/{MAX_WRONG_GUESSES}")
        self.wrong_label.setFont(QFont("Arial", 12))
        self.wrong_label.setStyleSheet("color: #e74c3c;")
        self.wrong_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.wrong_label)

        self.used_label = QLabel("Used letters: ")
        self.used_label.setFont(QFont("Arial", 10))
        self.used_label.setStyleSheet("color: #95a5a6;")
        self.used_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.used_label)

        self.clue_label = QLabel("Category: ???")
        self.clue_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.clue_label.setStyleSheet("color: #f39c12;")
        self.clue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.clue_label)

        keyboard = QWidget()
        keyboard_layout = QGridLayout(keyboard)
        keyboard_layout.setSpacing(4)
        self.letter_buttons: dict[str, QPushButton] = {}
        for i, letter in enumerate(LETTERS):
            button = QPushButton(letter)
            button.setFixedSize(36, 30)
            button.setStyleSheet(_letter_style("#3498db"))
            button.clicked.connect(lambda _checked, l=letter: self.guess_letter(l))
            keyboard_layout.addWidget(button, i // 9, i % 9)
            self.letter_buttons[letter] = button
        layout.addWidget(keyboard, alignment=Qt.AlignmentFlag.AlignHCenter)

        buttons = QHBoxLayout()
        buttons.setSpacing(20)

        clue_button = QPushButton("Show Clue")
        clue_button.setStyleSheet(_action_style("#f39c12", "#e67e22"))
        clue_button.clicked.connect(self.show_clue)
        buttons.addWidget(clue_button)

        new_game_button = QPushButton("New Game")
        new_game_button.setStyleSheet(_action_style("#27ae60", "#229954"))
        new_game_button.clicked.connect(self.new_game)
        buttons.addWidget(new_game_button)

        layout.addLayout(buttons)

    def new_game(self) -> None:
        self.secret_word = random.choice(list(WORD_CATEGORIES))
        self.secret_category = WORD_CATEGORIES[self.secret_word]
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.game_over = False
        self.clue_shown = False

        for button in self.letter_buttons.values():
            button.setEnabled(True)
            button.setStyleSheet(_letter_style("#3498db"))

        self.canvas.set_wrong_guesses(0)
        self.clue_label.setText("Category: ???")
        self.update_display()

    def guess_letter(self, letter: str) -> None:
        if self.game_over or letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)
        button = self.letter_buttons[letter]
        button.setEnabled(False)

        if letter in self.secret_word:
            button.setStyleSheet(_letter_style("#27ae60"))
        else:
            self.wrong_guesses += 1
            button.setStyleSheet(_letter_style("#e74c3c"))
            self.canvas.set_wrong_guesses(self.wrong_guesses)

        self.update_display()
        self.check_game_over()

    def update_display(self) -> None:
        display_word = " ".join(
            letter if letter in self.guessed_letters else "_" for letter in self.secret_word
        )
        self.word_label.setText(display_word)
        self.wrong_label.setText(f"Wrong guesses: {self.wrong_guesses}/{MAX_WRONG_GUESSES}")
        self.used_label.setText(f"Used letters: {' '.join(sorted(self.guessed_letters))}")

    def show_clue(self) -> None:
        if not self.clue_shown and not self.game_over:
            self.clue_shown = True
            self.clue_label.setText(f"Category: {self.secret_category}")

    def check_game_over(self) -> None:
        if all(letter in self.guessed_letters for letter in self.secret_word):
            self.game_over = True
            QMessageBox.information(
                self, "Congratulations!", f"You won! The word was: {self.secret_word}"
            )
            return

        if self.wrong_guesses >= MAX_WRONG_GUESSES:
            self.game_over = True
            QMessageBox.information(
                self, "Game Over", f"You lost! The word was: {self.secret_word}"
            )


def main() -> None:
    app = QApplication(sys.argv)
    window = HangmanWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
