# Supplied data dictionary

One row is one recorded over. Missing records are not zero-run records.

| Column | Meaning |
|---|---|
| `match_id` | Match identifier; bootstrap cluster key. |
| `match_date` | Date of match (YYYY-MM-DD). |
| `season_source` | Original season label. |
| `season_year` | Prepared numeric season year. |
| `innings` | Innings number within match. |
| `batting_team` | Team batting in this innings. |
| `bowling_team` | Opponent. |
| `over_number` | One-based over number; Powerplay covers 1–6. |
| `phase` | Prepared phase label. |
| `total_runs` | All runs in the over, including extras. |
| `batter_runs` | Runs credited to batters. |
| `extras` | Extras in the over. |
| `dismissals` | Recorded dismissals; not necessarily all charged to bowlers. |
| `dot_balls` | Recorded deliveries with zero total runs. |
| `fours` | Recorded batter four events. |
| `sixes` | Recorded batter six events. |
| `deliveries_recorded` | All recorded deliveries, including illegal deliveries. |
| `legal_balls` | Legal deliveries in the over. |
| `complete_over` | True when legal_balls is six; does not by itself establish complete powerplay coverage. |
| `venue` | Venue label. |
| `match_winner` | Winner where recorded. |
| `batting_team_won` | Whether batting team equals recorded winner; not used for this assignment. |
