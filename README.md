# Text Adventure

A command-line text adventure game written in Python. Explore rooms, examine and use objects, collect items, and solve a small chain of puzzles to progress.

## Running it

Requires Python 3.10+ (no external dependencies).

```bash
python main.py
```

## How to play

Type commands at the `▶` prompt. Movement can be done by direction or by naming a destination directly (e.g. `north`, `n`, `go north`, or `go garden`).

- `go <direction/location>` OR `<direction/location>` — Go somewhere
- `examine` OR `ex <item/object/etc>` — Examine the surroundings
- `use <object>` — Use something
- `use <item> on <object>` — Use a specific item on an object
- `take <item>` — Pick up an item and add it to your inventory
- `inventory` OR `inv` — Show your inventory
- `history` — View full command history
- `help` — Show the in-game help menu
- `quit` OR `exit` — End the game (progress is not saved)

Commands support partial matching — typing `examine paint` will resolve to `loose painting` if it's unambiguous, and the game will ask for clarification if multiple items match.

## Design notes

The game world (rooms, exits, items, and interactable objects) is defined entirely as data in `data.py`, keyed by enums from `enums.py`. Game logic in `world.py`, `interactions.py`, and `commands.py` operates generically over that data rather than hard-coding behavior per room — adding a new room or object is a matter of extending the data, not writing new branching logic.

Mutable game state (which objects have been used, which are currently visible, current inventory, etc.) is tracked separately from the static world definition, in `GameState` (`state.py`). The world data itself is never modified during play — game logic reads it as a template and checks/writes actual progress against the state object instead. This keeps the world definitions reusable and makes the game state easy to reason about (and, if extended, straightforward to serialize for a save/load feature).

Commands are dispatched through a lookup table (`COMMAND_DISPATCH` in `commands.py`) rather than a long chain of `if`/`elif` statements, keeping the parsing logic flat and easy to extend.

## Project structure

| File | Responsibility |
|---|---|
| `main.py` | Entry point and main game loop |
| `data.py` | World data — rooms, exits, items, interactables |
| `enums.py` | Enums used as keys/values throughout the game data and logic |
| `state.py` | `GameState` dataclass — all mutable player/game state |
| `commands.py` | Command parsing and dispatch |
| `world.py` | Movement, visibility, and "used" state helpers |
| `interactions.py` | Examine/use/take logic and interaction effects |
| `display.py` | Terminal output and room rendering |
| `logger.py` | Action log and full command history tracking |
| `utils.py` | Shared helpers (e.g. partial name resolution) |
