#!/usr/bin/env python3

import csv
import json
import re
import sys
import webbrowser
from datetime import datetime, timezone
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"

DRAFTS_FILE = DATA_DIR / "reports.json"
CSV_FILE = DATA_DIR / "report_drafts.csv"


REASONS = {
    "1": "Spam or scam",
    "2": "Impersonation",
    "3": "Harassment or bullying",
    "4": "Inappropriate content",
    "5": "Intellectual property concern",
    "6": "Other",
}


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_drafts():
    ensure_data_dir()

    if not DRAFTS_FILE.exists():
        return []

    try:
        with DRAFTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (OSError, json.JSONDecodeError):
        print("Warning: Could not read saved drafts.")
        return []


def save_drafts(drafts):
    ensure_data_dir()

    temp_file = DRAFTS_FILE.with_suffix(".tmp")

    try:
        temp_file.write_text(
            json.dumps(
                drafts,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        temp_file.replace(DRAFTS_FILE)

        try:
            DRAFTS_FILE.chmod(0o600)
        except OSError:
            pass

    except OSError as error:
        print(f"Could not save drafts: {error}")


def valid_username(username):
    username = username.removeprefix("@")

    return bool(
        re.fullmatch(
            r"[A-Za-z0-9._]{1,30}",
            username,
        )
    )


def ask_username():
    while True:
        username = input(
            "Instagram username (without @): "
        ).strip()

        username = username.removeprefix("@")

        if valid_username(username):
            return username

        print(
            "Invalid username. Use letters, numbers, dots "
            "or underscores."
        )


def choose_reason():
    print("\nAvailable reasons:")

    for key, reason in REASONS.items():
        print(f"  {key}. {reason}")

    while True:
        choice = input("\nChoose reason: ").strip()

        if choice in REASONS:
            return REASONS[choice]

        print("Invalid choice.")


def next_draft_id(drafts):
    ids = []

    for draft in drafts:
        try:
            ids.append(int(draft.get("id", 0)))
        except (TypeError, ValueError):
            pass

    return max(ids, default=0) + 1


def create_draft():
    print("\n" + "=" * 50)
    print("CREATE REPORT DRAFT")
    print("=" * 50)

    print(
        "\nOnly prepare a report for a genuine concern."
    )

    username = ask_username()
    reason = choose_reason()

    print(
        "\nDescribe the concern factually."
        "\nDo not enter passwords, login codes or cookies."
    )

    description = input(
        "Description: "
    ).strip()[:2000]

    evidence = input(
        "Evidence note/path (optional): "
    ).strip()[:500]

    draft = {
        "id": next_draft_id(load_drafts()),
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "username": username,

        "profile_url":
            f"https://www.instagram.com/{username}/",

        "reason": reason,

        "description": description,

        "evidence_note": evidence,

        "status": "draft_not_submitted",
    }

    print("\n" + "-" * 50)
    print("REVIEW")
    print("-" * 50)

    print(f"Username: @{draft['username']}")
    print(f"Profile: {draft['profile_url']}")
    print(f"Reason: {draft['reason']}")
    print(
        f"Description: "
        f"{draft['description'] or '(none)'}"
    )
    print(
        f"Evidence: "
        f"{draft['evidence_note'] or '(none)'}"
    )

    print(
        "\nThis program has NOT submitted a report."
    )

    confirm = input(
        "\nSave draft? [y/N]: "
    ).strip().lower()

    if confirm != "y":
        print("Draft discarded.")
        return

    drafts = load_drafts()
    drafts.append(draft)
    save_drafts(drafts)

    print(
        f"\nDraft #{draft['id']} saved."
    )


def view_drafts():
    drafts = load_drafts()

    print("\n" + "=" * 50)
    print("SAVED DRAFTS")
    print("=" * 50)

    if not drafts:
        print("No drafts found.")
        return

    for number, draft in enumerate(drafts, 1):
        print(
            f"\n[{number}] "
            f"Draft #{draft.get('id', '?')}"
        )

        print(
            f"Username: "
            f"@{draft.get('username', '')}"
        )

        print(
            f"Reason: "
            f"{draft.get('reason', '')}"
        )

        print(
            f"Status: "
            f"{draft.get('status', '')}"
        )

        print(
            f"Created: "
            f"{draft.get('created_at', '')}"
        )

        print(
            f"Description: "
            f"{draft.get('description', '')}"
        )


def delete_draft():
    drafts = load_drafts()

    if not drafts:
        print("No drafts available.")
        return

    view_drafts()

    choice = input(
        "\nEnter draft list number to delete: "
    ).strip()

    if not choice.isdigit():
        print("Invalid number.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(drafts):
        print("Draft not found.")
        return

    draft = drafts[index]

    confirm = input(
        f"Delete draft for "
        f"@{draft.get('username', '')}? [y/N]: "
    ).strip().lower()

    if confirm != "y":
        print("Cancelled.")
        return

    drafts.pop(index)
    save_drafts(drafts)

    print("Draft deleted.")


def export_csv():
    drafts = load_drafts()

    if not drafts:
        print("No drafts available.")
        return

    fields = [
        "id",
        "created_at",
        "username",
        "profile_url",
        "reason",
        "description",
        "evidence_note",
        "status",
    ]

    try:
        with CSV_FILE.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields,
                extrasaction="ignore",
            )

            writer.writeheader()
            writer.writerows(drafts)

        try:
            CSV_FILE.chmod(0o600)
        except OSError:
            pass

        print(
            f"Exported {len(drafts)} drafts."
        )
        print(f"File: {CSV_FILE}")

    except OSError as error:
        print(f"CSV export failed: {error}")


def review_drafts():
    drafts = load_drafts()

    if not drafts:
        print("No drafts available.")
        return

    print(
        "\nEach draft will be reviewed separately."
    )

    for index, draft in enumerate(drafts, 1):
        print("\n" + "=" * 50)
        print(
            f"DRAFT {index}/{len(drafts)}"
        )
        print("=" * 50)

        print(
            f"Username: "
            f"@{draft.get('username', '')}"
        )

        print(
            f"Profile: "
            f"{draft.get('profile_url', '')}"
        )

        print(
            f"Reason: "
            f"{draft.get('reason', '')}"
        )

        print(
            f"Description: "
            f"{draft.get('description', '')}"
        )

        print(
            f"Evidence: "
            f"{draft.get('evidence_note', '')}"
        )

        print(
            "\nNo report is submitted by this program."
        )

        action = input(
            "\n[Enter] next | "
            "[o] open profile | "
            "[q] quit: "
        ).strip().lower()

        if action == "q":
            break

        if action == "o":
            webbrowser.open(
                draft.get("profile_url", "")
            )

            input(
                "Press Enter for next draft..."
            )

    print("\nReview finished.")


def open_help_center():
    url = "https://help.instagram.com/"

    print(
        "\nOpening Instagram Help Center..."
    )

    webbrowser.open(url)


def show_about():
    print(
        """
Instagram Report Assistant
--------------------------

Purpose:
Prepare and organize report drafts locally.

This project:
- does not collect Instagram passwords
- does not collect login codes
- does not collect session cookies
- does not perform mass reporting
- does not automatically submit reports
- does not bypass Instagram controls

Final report submission is manual.
"""
    )


def continuous_draft_mode():
    print(
        "\nContinuous draft mode."
        "\nCreate one draft after another."
        "\nPress Ctrl+C to stop."
    )

    while True:
        try:
            create_draft()

            again = input(
                "\nCreate another draft? [Y/n]: "
            ).strip().lower()

            if again == "n":
                break

        except KeyboardInterrupt:
            print(
                "\nContinuous mode stopped."
            )
            break


def main():
    ensure_data_dir()

    while True:
        print("\n")
        print("=" * 55)
        print("        INSTAGRAM REPORT ASSISTANT")
        print("             MULTI-DRAFT CLI")
        print("=" * 55)

        print("1. Add report draft")
        print("2. View all drafts")
        print("3. Review drafts one by one")
        print("4. Delete draft")
        print("5. Export drafts to CSV")
        print("6. Continuous draft mode")
        print("7. Open Instagram Help Center")
        print("8. About")
        print("9. Exit")

        choice = input(
            "\nSelect option: "
        ).strip()

        if choice == "1":
            create_draft()

        elif choice == "2":
            view_drafts()

        elif choice == "3":
            review_drafts()

        elif choice == "4":
            delete_draft()

        elif choice == "5":
            export_csv()

        elif choice == "6":
            continuous_draft_mode()

        elif choice == "7":
            open_help_center()

        elif choice == "8":
            show_about()

        elif choice == "9":
            print("Goodbye.")
            break

        else:
            print(
                "Invalid option. "
                "Choose 1-9."
            )

        input(
            "\nPress Enter to continue..."
        )


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nExited safely.")

    except EOFError:
        print("\nInput closed.")

    sys.exit(0)
