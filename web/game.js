export const MAX_WRONG = 6;

export function createRound(words, rng = Math.random) {
  const selected = words[Math.floor(rng() * words.length)];
  return {
    word: selected.word,
    category: selected.category,
    guessed: [],
    wrongGuesses: 0,
    gameOver: false,
    won: false,
    clueShown: false,
  };
}

export function guessLetter(round, letter) {
  const normalized = letter.toUpperCase();
  if (round.gameOver || round.guessed.includes(normalized)) {
    return { hit: false, finished: null };
  }

  round.guessed.push(normalized);
  const hit = round.word.includes(normalized);
  if (!hit) {
    round.wrongGuesses += 1;
  }

  if (round.word.split("").every((character) => round.guessed.includes(character))) {
    round.gameOver = true;
    round.won = true;
    return { hit: true, finished: "won" };
  }

  if (round.wrongGuesses >= MAX_WRONG) {
    round.gameOver = true;
    round.won = false;
    return { hit: false, finished: "lost" };
  }

  return { hit, finished: null };
}

export function maskedWord(round) {
  return round.word
    .split("")
    .map((letter) => (round.guessed.includes(letter) ? letter : "_"))
    .join(" ");
}

export function showClue(round) {
  if (round.gameOver || round.clueShown) {
    return null;
  }
  round.clueShown = true;
  return round.category;
}
