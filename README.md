# massreportinginstagram
# Instagram Report Assistant

A Linux-compatible command-line assistant for preparing and organizing
Instagram report drafts.

## Features

- Interactive terminal CLI
- One report draft at a time
- Continuous draft mode
- Multiple saved drafts
- Draft review
- Draft deletion
- CSV export
- Local JSON storage
- Instagram profile opening
- Instagram Help Center shortcut
- Python standard library only

## Safety and privacy

This project intentionally does NOT:

- collect Instagram passwords
- collect login codes
- collect session cookies
- create fake Instagram login pages
- automate mass reporting
- repeatedly submit reports
- bypass Instagram protections
- submit reports automatically

The application only prepares and organizes drafts locally.

Final submission must be performed manually using Instagram's
official interface.

## Requirements

- Linux
- Python 3.9 or newer
- A browser
- Git (optional)

No third-party Python packages are required.

## Installation

Clone the repository:

    git clone https://github.com/YOUR_USERNAME/instagram-report-assistant.git

Enter the directory:

    cd instagram-report-assistant

Create virtual environment:

    python3 -m venv .venv

Activate it:

    source .venv/bin/activate

Run:

    python3 app.py

## Quick start

You can also use:

    chmod +x run.sh
    ./run.sh

## Menu

    1. Add report draft
    2. View all drafts
    3. Review drafts one by one
    4. Delete draft
    5. Export drafts to CSV
    6. Continuous draft mode
    7. Open Instagram Help Center
    8. About
    9. Exit

## Continuous draft mode

Continuous draft mode lets you prepare multiple drafts without
returning to the main menu.

It does NOT continuously submit reports to Instagram.

Press Ctrl+C to stop the mode.

## Local data

Drafts are stored in:

    data/reports.json

CSV exports are stored in:

    data/report_drafts.csv

These files are ignored by Git because they may contain usernames
or evidence notes.

## Testing

Run:

    python3 -m unittest discover -s tests -v

## GitHub setup

Initialize Git:

    git init

Add files:

    git add .

Commit:

    git commit -m "Initial release"

Set main branch:

    git branch -M main

Add GitHub remote:

    git remote add origin https://github.com/YOUR_USERNAME/instagram-report-assistant.git

Push:

    git push -u origin main

Replace YOUR_USERNAME with your GitHub username.

## Project structure

    instagram-report-assistant/
    |
    |-- app.py
    |-- requirements.txt
    |-- README.md
    |-- LICENSE
    |-- .gitignore
    |-- run.sh
    |
    |-- data/
    |   `-- .gitkeep
    |
    `-- tests/
        `-- test_app.py

## Disclaimer

This is an independent local utility and is not affiliated with
Instagram or Meta.

Use reporting features only for genuine concerns and provide
accurate information.
