## Purpose
Provide concise, actionable guidance for AI coding agents working on this interactive board-game Python project.

## Quick start
- **Run locally:** Use Python 3 to run the CLI entrypoint: `python3 main.py` ([main.py](main.py)).
- **No test suite:** There are no automated tests or build steps; changes should be smoke-tested by running the CLI flows.

## Big-picture architecture
- **Entrypoint:** [main.py](main.py) instantiates `Game_Manager` and drives the program.
- **Manager layer:** `Game_Manager` ([Games_Manager.py](Games_Manager.py)) holds application state: `players_dict`, `groups_dict`, and `games_history_list`. It provides the interactive menus and orchestrates flows.
- **Domain models:** `Player`, `Group`, `Game` live in [Games_Manager.py](Games_Manager.py). `New_Game` (game engine/round logic and board handling) is implemented in [New_Game.py](New_Game.py).
- **Integration point:** `Game` uses `New_Game` to perform the low-level game play; changes to `New_Game` directly affect play results and durations.

## Project-specific conventions & patterns
- **Interactive CLI-first design:** The code is driven entirely by blocking `input()` calls and `print()` statements. Edits must preserve conversational prompts and expected input shapes.
- **In-memory canonical state:** Players and groups are keyed by name strings in dictionaries (`players_dict`, `groups_dict`) — names are the identity used throughout the app.
- **Simple selection/sorting implementations:** Sorting is implemented manually (selection-style loops) in `_sort_players_by_score` and `_sort_groups_by_score` — expect O(n^2) loops on small datasets.
- **Tree structure for groups:** `Group` objects maintain `mother_group` and `sub_groups` to represent nested groups; `get_total_score()` aggregates recursively.

## Notable gotchas & observable bugs (useful for code changes)
- New_Game duration: `New_Game._start_new_game` sets `self.duration = duration_delta.total_seconds` (missing `()`), so duration becomes a method object, not a float. See [New_Game.py](New_Game.py).
- Game vs caller mismatch: `Game.__init__` expects `Player` objects, but some call sites pass names (strings). Search for `Game(` usage in [Games_Manager.py](Games_Manager.py) — validate types before refactors.
- Input parsing risks: numeric conversions (e.g., `int(input(...))`) assume valid input and will crash on non-numeric input. Add defensive parsing when adding tests or refactors.
- `_number_validation` in `New_Game` converts characters to `int` after skipping `.`; be cautious about non-digit characters raising `ValueError`.

## What to change and examples
- Small bugfix example (duration): In [New_Game.py](New_Game.py), change `self.duration = duration_delta.total_seconds` to `self.duration = duration_delta.total_seconds()`.
- Type-safety example: When constructing `Game`, prefer passing `Player` objects rather than names; update `create_new_game()` to call `Game(player1, player2)` and adjust `Game` internals if it currently expects strings.
- Defensive input parsing: wrap `int(input(...))` calls with helper `safe_int(prompt, min=None, max=None)` that loops until valid input.

## Editing guidance for AI agents
- Preserve interactive prompts and return values for functions that are part of the CLI flows. Changing interfaces will require updating multiple menu handlers in [Games_Manager.py](Games_Manager.py).
- Make minimal, focused edits. Run the CLI flows after changes: create players, start a game, check `glory_hall` and `games_history` to verify behavioural changes.
- When renaming keys used as identities (player names), update all dictionary usages and consider collisions (`players_dict` keys are unique names).

## Files to inspect for larger changes
- Core manager and models: [Games_Manager.py](Games_Manager.py)
- Game engine: [New_Game.py](New_Game.py)
- Entrypoint: [main.py](main.py)

## When you need clarification
- Ask about desired behaviours for edge-cases: how to handle duplicate names, whether `Game` should accept names or `Player` objects, and whether duration should be stored in seconds or an ISO timestamp.

---
If anything above is unclear or you'd like the instructions to assume stricter typing, tests, or a CI workflow, tell me which direction and I'll iterate.
