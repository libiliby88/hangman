import { createRound, guessLetter, MAX_WRONG, maskedWord, showClue } from "./game.js";

const results = document.querySelector("#results");
const summary = document.querySelector("#summary");
let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function test(name, callback) {
  const item = document.createElement("li");
  try {
    callback();
    passed += 1;
    item.className = "pass";
    item.textContent = `PASS: ${name}`;
  } catch (error) {
    failed += 1;
    item.className = "fail";
    item.textContent = `FAIL: ${name} — ${error.message}`;
  }
  results.append(item);
}

const words = [{ word: "HANGMAN", category: "Game" }];

test("createRound chooses the word and resets state", () => {
  const round = createRound(words, () => 0);
  assert(round.word === "HANGMAN", "word should be selected");
  assert(round.category === "Game", "category should be copied");
  assert(round.guessed.length === 0 && round.wrongGuesses === 0, "state should reset");
});

test("maskedWord hides and reveals letters", () => {
  const round = createRound(words, () => 0);
  assert(maskedWord(round) === "_ _ _ _ _ _ _", "word should start masked");
  guessLetter(round, "a");
  assert(maskedWord(round) === "_ A _ _ _ A _", "all matching letters should show");
});

test("repeat guesses are ignored", () => {
  const round = createRound(words, () => 0);
  guessLetter(round, "A");
  const before = JSON.stringify(round);
  const result = guessLetter(round, "A");
  assert(result.hit === false && result.finished === null, "repeat should be ignored");
  assert(JSON.stringify(round) === before, "repeat should not change state");
});

test("six wrong guesses lose", () => {
  const round = createRound(words, () => 0);
  for (const letter of ["B", "C", "D", "E", "F", "J"]) {
    guessLetter(round, letter);
  }
  assert(round.gameOver && !round.won, "round should be lost");
  assert(round.wrongGuesses === 6, "wrong count should reach six");
});

test("full word wins", () => {
  const round = createRound([{ word: "AB", category: "Test" }], () => 0);
  assert(guessLetter(round, "A").finished === null, "first letter should continue");
  assert(guessLetter(round, "B").finished === "won", "last letter should win");
});

test("post-gameover guesses are ignored", () => {
  const round = createRound([{ word: "A", category: "Test" }], () => 0);
  guessLetter(round, "A");
  const before = JSON.stringify(round);
  const result = guessLetter(round, "B");
  assert(result.finished === null && JSON.stringify(round) === before, "gameover should freeze state");
});

test("clue is available once only", () => {
  const round = createRound(words, () => 0);
  assert(showClue(round) === "Game", "first clue should return category");
  assert(showClue(round) === null, "second clue should be unavailable");
});

summary.textContent = `${passed} passed, ${failed} failed`;
summary.className = failed ? "fail" : "pass";
console.log(`${passed} passed, ${failed} failed`);
