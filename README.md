# tiny-chess-4k

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/8kunoir8/tiny-chess-4k/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/8kunoir8/tiny-chess-4k/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in under 4 KB of Python: 0x88 board, iterative-deepening alpha-beta with quiescence, a transposition table, killer moves and check extensions, Zobrist repetition and fifty-move draw detection, and a material + piece-square evaluation with an endgame king table. Search is budgeted in wall-clock, not nodes: a per-game manager splits a 110-second allowance across the game's moves and converts each share into a node limit using the engine's measured search speed, so every game finishes inside the 120-second wall budget on fast and slow machines alike. `main.py` is the lzma-packed form of the submitted engine source; the kit's `compress` command reproduces it byte for byte.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8080 python main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=2zer828j&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
