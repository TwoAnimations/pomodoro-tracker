# Pomodoro Tracker CLI

A command-line productivity app for running focus sessions and tracking progress.

## What this project demonstrates

- Building practical CLI tools with `argparse`.
- Working with JSON persistence.
- Basic metrics aggregation for user activity.
- Clean command design (`start`, `stats`, `history`).

## Stack

- Python 3.10+
- Standard library only

## Files

- `tracker.py` - all CLI commands.
- `sessions.json` - auto-generated storage file.

## Run locally

```bash
cd pomodoro-tracker
python3 tracker.py start
```

Default session length: `25` minutes.

## Commands

### Start a session

```bash
python3 tracker.py start
python3 tracker.py start --minutes 50 --label "Deep Work"
```

### Show aggregated statistics

```bash
python3 tracker.py stats
```

### Show recent sessions

```bash
python3 tracker.py history
python3 tracker.py history --limit 5
```

## Example stats output

```text
Total sessions: 8
Completed: 6
Interrupted: 2
Total focus time: 4h 10m 0s
```

## Possible improvements

- Auto break sessions (short/long).
- Desktop notifications.
- CSV export.
- Daily goals and streaks.
