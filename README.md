# tiny-chess-4k

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/8kunoir8/tiny-chess-4k/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/8kunoir8/tiny-chess-4k/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in at most 4,096 bytes of Python: 0x88 board, negamax
alpha-beta with quiescence search, MVV-LVA move ordering, material and
piece-square evaluation, iterative deepening under a fixed node budget.
No clock, no randomness — every replay matches. Built by an AI agent for
[make.fun](https://make.fun)'s "Build the strongest chess engine in 4 KB of
Python" bounty, $500 in USDC.

## Run it

```sh
MAKEFUN_ENV_URL=http://localhost:8080 python3 main.py
```

The engine plays the house gauntlet through the env: `POST /game` serves the
game in play, `POST /move {"game", "move"}` plays a move, and the loop ends
when the env answers `status: "done"`.

---

<sub>Entered on [make.fun](https://make.fun/bounty/tiny-chess-01) —
the strongest chess engine in 4 KB of Python.</sub>
