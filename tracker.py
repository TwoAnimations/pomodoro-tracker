#!/usr/bin/env python3
import argparse
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

DATA_PATH = Path(__file__).with_name("sessions.json")


def load_sessions():
    if not DATA_PATH.exists():
        return []
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def save_sessions(sessions):
    DATA_PATH.write_text(json.dumps(sessions, indent=2), encoding="utf-8")


def format_seconds(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {sec}s"
    return f"{minutes}m {sec}s"


def run_timer(minutes: int, label: str):
    total_seconds = minutes * 60
    start = datetime.now()
    end = start + timedelta(seconds=total_seconds)

    print(f"Starting: {label}")
    print(f"Duration: {minutes} minutes")

    try:
        while True:
            now = datetime.now()
            left = int((end - now).total_seconds())
            if left <= 0:
                break
            print(f"\rTime left: {format_seconds(left)}", end="", flush=True)
            time.sleep(1)
        print("\rTime left: 0m 0s")
    except KeyboardInterrupt:
        elapsed = int((datetime.now() - start).total_seconds())
        print("\nSession interrupted.")
        return {
            "label": label,
            "start": start.isoformat(timespec="seconds"),
            "duration_minutes": minutes,
            "elapsed_seconds": elapsed,
            "completed": False,
        }

    print("Session completed.")
    return {
        "label": label,
        "start": start.isoformat(timespec="seconds"),
        "duration_minutes": minutes,
        "elapsed_seconds": total_seconds,
        "completed": True,
    }


def cmd_start(args):
    session = run_timer(args.minutes, args.label)
    sessions = load_sessions()
    sessions.append(session)
    save_sessions(sessions)
    print("Saved session to sessions.json")


def cmd_stats(_args):
    sessions = load_sessions()
    if not sessions:
        print("No sessions yet.")
        return

    total = len(sessions)
    completed = sum(1 for s in sessions if s["completed"])
    interrupted = total - completed
    total_seconds = sum(s["elapsed_seconds"] for s in sessions)

    print(f"Total sessions: {total}")
    print(f"Completed: {completed}")
    print(f"Interrupted: {interrupted}")
    print(f"Total focus time: {format_seconds(total_seconds)}")


def cmd_history(args):
    sessions = load_sessions()
    if not sessions:
        print("No sessions yet.")
        return

    limit = args.limit
    for s in sessions[-limit:]:
        status = "done" if s["completed"] else "stopped"
        print(
            f"[{s['start']}] {s['label']} - {status} - "
            f"{format_seconds(s['elapsed_seconds'])}"
        )


def build_parser():
    parser = argparse.ArgumentParser(description="Pomodoro tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="start a timer")
    start_parser.add_argument("-m", "--minutes", type=int, default=25)
    start_parser.add_argument("-l", "--label", default="Focus session")
    start_parser.set_defaults(func=cmd_start)

    stats_parser = subparsers.add_parser("stats", help="show summary stats")
    stats_parser.set_defaults(func=cmd_stats)

    history_parser = subparsers.add_parser("history", help="show session history")
    history_parser.add_argument("-n", "--limit", type=int, default=10)
    history_parser.set_defaults(func=cmd_history)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

