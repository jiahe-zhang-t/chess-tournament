# Chess Agent Competition Public Rules

Rules version 1.1 dated September 4, 2026

These rules govern the Chess Agent Competition Track for ECE-GY 6263. The published scoring formulas, clocks, resource limits, fault rules, matchup memory, and playoff format remain fixed through the submission freeze and tournament.

## Participation and submission

The Chess track is an individual Option 3 project. Each student uploads exactly one self-contained Python file to the designated Gradescope assignment. The file is named with the student's NYU NetID, such as `abc123.py`, must be at most 1 MiB, and must define exactly one no-argument subclass of the supplied `ChessAgent` interface. The starter ZIP, virtual environments, and source-code archives are not submissions.

The only third-party dependency available to an agent is `chess==1.11.2`. External engines, network services, subprocesses, model files, additional data files, and access to other submissions are prohibited.

The public alias in `ChessAgent.name` must be a plain string of 1–40 ASCII letters, digits, spaces, periods, underscores, or hyphens, beginning with a letter or digit. Invalid aliases fail validation; duplicate valid aliases may receive an instructor-added display suffix. The validator rejects imports whose top-level name is `ctypes`, `ftplib`, `http`, `multiprocessing`, `requests`, `socket`, `subprocess`, or `urllib`.

## Public agent interface

The official API version is `1.0`. A fresh agent instance is created for every matchup. The same instance persists across games within that matchup and is destroyed afterward.

A benchmark matchup consists of one student agent against one benchmark variant for eight games. A league matchup consists of four games between one pair of students from two frozen, color-reversed starting positions. A playoff matchup consists of the complete scheduled series plus any tiebreak games. Repeated opponents in later stages start a new matchup with a new anonymous `opponent_id`.

The `opponent_id` is stable only within the current matchup and does not reveal a name or NetID. `initialize` is called at the start of every game. `on_game_end` is called after each completed game. State may persist only through these callbacks within the current matchup.

`choose_move` must return a plain Python string containing legal UCI. The encoded response is limited to 32 bytes; legal UCI normally requires four or five ASCII characters.

The `GameResult` delivered to `on_game_end` is recipient-relative and contains only an opaque `game_id`, the matchup-local `opponent_id`, self/opponent color and scores, normalized outcome and fault side, moves, remaining clocks, starting FEN, seed, and matchup game index. It contains no real identity, internal participant ID, opponent alias, or PGN metadata.

## Clock and resources

The official limits are:

```text
Initial clock             10.0 seconds per player
Increment                  0.1 seconds after each accepted legal move
choose_move hard cap       5.0 seconds per call
initialize cap             1.0 second per call
on_game_end cap            0.5 second per call
Maximum length           500 plies
CPU                        1 vCPU per agent
Memory                   512 MiB per agent
Network                    disabled
GPU                        unavailable
Additional processes       prohibited
Submission mount           read only
```

For `choose_move`, the controller measures monotonic wall time from request dispatch through receipt of a valid bounded response. The callback deadline is the earlier of the remaining chess clock and the 5.0 second hard cap. Time used is deducted from the chess clock; the increment is added only after the controller accepts a legal move. Workers receive no CPU entitlement outside permitted callbacks in the official environment.

## Fault and adjudication policy

An illegal or malformed UCI move, non-string or oversized return value, exception, process exit, move hard-cap violation, exhausted chess clock, initialization failure, memory violation, or other attributable resource violation forfeits the current game.

After an `initialize` or worker failure, the failed agent starts the next game in a fresh worker and loses prior matchup state. An `on_game_end` failure does not change the completed game's score, but records a fault and causes the affected agent to restart before the next game. A runtime fault does not automatically remove an otherwise valid submission from later games. Deliberate security violations may be referred under course policy and may cause disqualification.

If both agents fail initialization before a game begins, the game is a double forfeit and each receives zero points. A controller or infrastructure failure is never charged to a student. To preserve matchup-local adaptation semantics, all provisional games in the affected matchup are discarded and that complete matchup is replayed from fresh processes with the same frozen fixture IDs, openings, colors, and seeds.

The controller automatically applies checkmate, stalemate, insufficient material, claimable threefold repetition, the claimable fifty-move rule, and other standard `python-chess` game-over conditions. Reaching 500 plies is a draw.

## Hidden benchmark evaluation

Each valid submission plays 32 benchmark games against four instructor-side variants: two Standard and two Advanced. Each variant plays four paired starting positions, once with the student as White and once with the student as Black. All students receive the same suite.

```text
B = 100 times benchmark points divided by 32
```

Public Random and Greedy agents support local development and do not count toward `B`.

## Student qualification league

Every unordered pair of valid student agents plays four games using the same two frozen legal league starting positions. Each position is used for one game with A as White and one game with B as White. The scheduled order is opening 1 with A-White, opening 1 with B-White, opening 2 with B-White, and opening 2 with A-White. This gives each agent one early and one late game with each color, makes all four games informative for deterministic agents, and preserves matchup-local adaptation. The exact positions are hidden during development and frozen before submission.

For `N >= 2`:

```text
R = 100 * league points / [4(N - 1)]
Q = 0.5B + 0.5R
```

The denominator is `4(N - 1)`. Calculations retain exact precision and are rounded only for display. For `N = 1`, `Q = B`; no league or championship bracket is held.

Qualification ties are resolved by higher `R`, then higher `B`, then league points earned within the still-tied group, then fewer official faults, then a deterministic draw derived from a seed frozen before submission. The tied-group rule remains well-defined for three-way and larger ties.

## Playoff field and series

For `N >= 4`, the playoff field is the largest supported power of two not exceeding half the valid roster, capped at 16. For `N = 2-3`, the field contains both valid agents. The following table is the authoritative field-size rule.

| Valid agents | Playoff field |
|---:|---:|
| 32 or more | 16 |
| 16 through 31 | 8 |
| 8 through 15 | 4 |
| 2 through 7 | 2 |
| Fewer than 2 | No champion |

Seeds pair highest against lowest. Round-of-16 and quarterfinal series schedule four games, semifinals six, and the final eight. Every two-game pair uses the same legal starting position with colors reversed. Early rounds receive one additional two-game pair when tied and then advance the higher seed if still tied. The final may receive up to three additional pairs before the higher-seed fallback.

## Final placement and Tournament Performance

Final placement is stage first and `Q` within the same eliminated stage: Champion, runner-up, semifinal losers, quarterfinal losers, Round-of-16 losers, then nonqualifiers.

| Placement | Tournament Performance out of 10 |
|---|---:|
| Champion | 10.0 |
| Runner-up | 9.5 |
| Semifinal loser | `8.8 + 0.4Q/100` |
| Quarterfinal loser | `8.2 + 0.5Q/100` |
| Round-of-16 loser | `7.6 + 0.5Q/100` |
| Nonqualifier | `7.5Q/100` |
| Missing or invalid official submission | 0.0 |

The champion therefore receives the unique maximum Tournament Performance score. This is a 10-point component of the Term Project rubric, not the entire project grade.

For `N = 1`, no championship title is awarded and the sole valid agent receives the nonqualifier score with `Q = B`.

## Public and hidden information

The public rules disclose formulas, game counts, color balance, clocks, resource limits, fault handling, matchup memory, bracket selection, tiebreaks, and scoring. Exact benchmark source, search parameters, benchmark, league, and playoff starting positions, seeds, execution order, and security internals may remain hidden.

Before the submission freeze, the instructor archives a digest covering the runner revision, public and secret configuration, hidden baselines, opening suite, seeds, and execution environment. Hidden test cases may remain private; grading rules may not change after the freeze.
