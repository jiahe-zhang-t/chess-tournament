# Chess Competition Rules

## Submission

Work individually. Submit one Python file on Gradescope, named with your NetID, such as `abc123.py`. The file must be at most 1 MiB and contain one `ChessAgent` subclass that takes no constructor arguments. Do not submit the Starter ZIP or a folder.

Use the supplied Agent API and Python standard library. The only additional library is `chess==1.11.2`. External chess engines, online services, model weights, extra data files, other submissions, and additional processes are not allowed.

Set `ChessAgent.name` to a nickname, not your name, NetID, or email. Use 1 to 40 ASCII letters, digits, spaces, periods, underscores, or hyphens. Start with a letter or digit. Invalid names fail validation. Staff may add a suffix to distinguish duplicate names.

## Agent behavior

A matchup is one complete series against one opponent. Your agent may remember previous games within that series. It starts fresh against the next opponent or when facing the same opponent in a later stage.

Use `initialize` at the start of each game, `choose_move` to return a legal UCI move as a plain Python string, and `on_game_end` to learn from the result. The move response must be at most 32 bytes. The Student Guide describes the API and allowed imports.

Your agent receives game information and an anonymous opponent ID that lasts only for that matchup. It never receives another student's identity or public agent name. It may run only during these callbacks.

## Time and resource limits

| Limit | Allowance per agent |
|---|---|
| Starting clock | 10 seconds per game |
| Time added after a legal move | 0.1 seconds |
| One move decision | 5 seconds or the remaining clock, whichever is less |
| Game initialization | 1 second |
| End of game callback | 0.5 seconds |
| CPU | 1 vCPU |
| Memory | 512 MiB |

Move time includes sending the request and receiving a valid response. It is deducted from your clock. The increment is added only after a legal move is accepted. Network and GPU access are disabled. Submission files are read only.

## Game results and errors

A win earns 1 point, a draw 0.5, and a loss 0. Standard chess endings apply. The system automatically claims draws for threefold repetition and the fifty-move rule. A game also ends in a draw after 500 half-moves, meaning 500 individual turns.

An illegal or invalid move, exception, crash, initialization failure, expired clock, or resource-limit violation loses the current game. Both agents receive 0 points if both fail initialization.

An initialization or worker failure restarts the affected agent before its next game, clearing its memory. An end of game callback failure also triggers a restart and counts as a fault, but does not change the completed result. An error does not automatically remove an otherwise valid agent from later games. Deliberate security violations may lead to disqualification and action under course policy.

Platform failures are not charged to students. Staff discard the affected matchup's provisional results and replay the entire series with fresh agents and the same openings, colors, game identifiers, and random seeds.

## Initial ranking

Each valid agent plays two sets of games.

- Instructor opponents: 32 games against four opponents, two Standard and two Advanced. Against each opponent, play four starting positions once as White and once as Black. B is your percentage of the 32 available points. Random and Greedy practice games do not count.
- Classmates: four games against every other valid student agent. Each pair uses two starting positions with colors reversed. R is your percentage of the points available across these games.

Your initial score Q is the average of B and R. Scores keep full precision until displayed.

All students use the same test sets. In each classmate matchup, the first-listed agent plays White, Black, Black, then White. Games 1 and 2 share the first opening. Games 3 and 4 share the second. Exact instructor agents, starting positions, and random seeds are not released during development. Staff fix the evaluation setup before the submission deadline. Grading rules remain unchanged after that deadline.

Ties are decided by higher R, then higher B, then points earned against the students still tied, then fewer official faults, then a reproducible random draw fixed before submission.

If only one agent is valid, its initial score is B. There are no classmate games, knockout rounds, or champion.

## Knockout rounds

The highest-ranked agents advance according to the number of valid submissions.

| Valid agents | Agents advancing |
|---|---|
| 32 or more | 16 |
| 16 through 31 | 8 |
| 8 through 15 | 4 |
| 2 through 7 | 2 |
| Fewer than 2 | No champion |

The highest-ranked entrant faces the lowest-ranked entrant, and so on. Each two-game pair uses the same starting position with colors reversed. The agent with more points wins the series and advances.

| Round | Scheduled games | Extra games if tied |
|---|---|---|
| Round of 16 | 4 | One pair |
| Quarterfinal | 4 | One pair |
| Semifinal | 6 | One pair |
| Final | 8 | Up to three pairs |

Each extra pair contains two games. If the series is still tied after these games, the agent with the higher initial ranking advances or wins the final.

## Final ranking and score

The final winner is champion and the other finalist is runner-up. Everyone else is ranked by the round reached, then by initial score Q among agents eliminated in the same round. Agents who did not advance follow those who reached the knockout rounds.

Tournament Performance contributes 10 points to the term project grade.

| Result | Points out of 10 |
|---|---|
| Champion | 10.0 |
| Runner-up | 9.5 |
| Eliminated in semifinal | 8.8 + 0.4Q/100 |
| Eliminated in quarterfinal | 8.2 + 0.5Q/100 |
| Eliminated in round of 16 | 7.6 + 0.5Q/100 |
| Did not advance | 7.5Q/100 |
| Missing or invalid submission | 0.0 |

Q is your initial score from 0 to 100. With one valid agent, use Q = B and the score for not advancing.
