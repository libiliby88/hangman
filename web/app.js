import { createRound, guessLetter, MAX_WRONG, maskedWord, showClue } from "./game.js";
import { WORDS } from "./words.js";

const BACKGROUND = "#2c3e50";
const TEXT = "#ecf0f1";
const canvas = document.querySelector("#hangman-canvas");
const context = canvas.getContext("2d");
const wordElement = document.querySelector("#word");
const wrongElement = document.querySelector("#wrong-count");
const usedElement = document.querySelector("#used-letters");
const clueElement = document.querySelector("#clue");
const keyboardElement = document.querySelector("#keyboard");
const clueButton = document.querySelector("#clue-button");
const newGameButton = document.querySelector("#new-game-button");
const resultDialog = document.querySelector("#result-dialog");
const resultTitle = document.querySelector("#result-title");
const resultMessage = document.querySelector("#result-message");
const resultAgainButton = document.querySelector("#result-again");
const resultCloseButton = document.querySelector("#result-close");

let round = null;
const letterButtons = new Map();

function drawLine(x1, y1, x2, y2) {
  context.beginPath();
  context.moveTo(x1, y1);
  context.lineTo(x2, y2);
  context.stroke();
}

function drawGallows() {
  context.clearRect(0, 0, 200, 200);
  context.lineWidth = 3;
  context.strokeStyle = TEXT;
  drawLine(20, 180, 100, 180);
  drawLine(60, 180, 60, 20);
  drawLine(60, 20, 120, 20);
  drawLine(120, 20, 120, 40);
}

function drawHangman() {
  drawGallows();
  context.strokeStyle = TEXT;
  context.lineWidth = 3;
  if (round.wrongGuesses >= 1) {
    context.beginPath();
    context.arc(120, 55, 15, 0, Math.PI * 2);
    context.stroke();
  }
  if (round.wrongGuesses >= 2) {
    drawLine(120, 70, 120, 120);
  }
  if (round.wrongGuesses >= 3) {
    drawLine(120, 80, 90, 100);
  }
  if (round.wrongGuesses >= 4) {
    drawLine(120, 80, 150, 100);
  }
  if (round.wrongGuesses >= 5) {
    drawLine(120, 120, 90, 150);
  }
  if (round.wrongGuesses >= 6) {
    drawLine(120, 120, 150, 150);
  }
}

function render() {
  wordElement.textContent = maskedWord(round);
  wrongElement.textContent = `Wrong guesses: ${round.wrongGuesses}/${MAX_WRONG}`;
  usedElement.textContent = `Used letters: ${[...round.guessed].sort().join(" ")}`;
  clueElement.textContent = `Category: ${round.clueShown ? round.category : "???"}`;
  drawHangman();
}

function setButtonState(letter, hit) {
  const button = letterButtons.get(letter);
  if (!button) {
    return;
  }
  button.disabled = true;
  button.classList.add(hit ? "correct" : "wrong");
}

function guess(letter) {
  if (!round || round.gameOver) {
    return;
  }
  const normalized = letter.toUpperCase();
  if (round.guessed.includes(normalized)) {
    return;
  }
  const result = guessLetter(round, normalized);
  setButtonState(normalized, result.hit);
  render();
  if (result.finished) {
    showResult(result.finished === "won");
  }
}

function showResult(won) {
  resultTitle.textContent = won ? "Congratulations!" : "Game Over";
  resultMessage.textContent = won
    ? `You won! The word was: ${round.word}`
    : `You lost! The word was: ${round.word}`;
  if (typeof resultDialog.showModal === "function") {
    resultDialog.showModal();
  } else {
    resultDialog.setAttribute("open", "");
  }
}

function closeResult() {
  if (resultDialog.open && typeof resultDialog.close === "function") {
    resultDialog.close();
  } else {
    resultDialog.removeAttribute("open");
  }
}

function startNewGame() {
  closeResult();
  round = createRound(WORDS);
  letterButtons.forEach((button) => {
    button.disabled = false;
    button.classList.remove("correct", "wrong");
  });
  clueElement.textContent = "Category: ???";
  render();
}

function createKeyboard() {
  "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").forEach((letter) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "letter-button";
    button.textContent = letter;
    button.addEventListener("click", () => guess(letter));
    keyboardElement.append(button);
    letterButtons.set(letter, button);
  });
}

function resizeCanvas() {
  const ratio = window.devicePixelRatio || 1;
  canvas.width = Math.round(200 * ratio);
  canvas.height = Math.round(200 * ratio);
  canvas.style.width = "200px";
  canvas.style.height = "200px";
  context.setTransform(ratio, 0, 0, ratio, 0, 0);
  drawHangman();
}

clueButton.addEventListener("click", () => {
  if (showClue(round) !== null) {
    render();
  }
});
newGameButton.addEventListener("click", startNewGame);
resultAgainButton.addEventListener("click", startNewGame);
resultCloseButton.addEventListener("click", closeResult);
window.addEventListener("keydown", (event) => {
  if (/^[a-z]$/i.test(event.key)) {
    event.preventDefault();
    guess(event.key);
  }
});
window.addEventListener("resize", resizeCanvas);

createKeyboard();
startNewGame();
resizeCanvas();

if ("serviceWorker" in navigator &&
    (window.isSecureContext || location.hostname === "localhost" || location.hostname === "127.0.0.1")) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}
