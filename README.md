# CCCS 106 — Application Development Labs

Year 3 Python and Flet course labs covering calculators, GUI forms, databases, contacts and weather.

**Portfolio:** [Carl Renz Colico](https://github.com/renzkie8) · **Year / Section:** Year 3 — BSCS 3-A

## Methodology

Build progressively larger Flet applications, add local database operations and connect a weather-service client.

## Results and limitations

The local archive matches existing GitHub source after line-ending normalization. Course structure is retained; student identifiers and local contact database are removed from the publication tree.

This upload documents the supplied submission. Experiments, model training, graphical interfaces and external services were not fully rerun during portfolio preparation. See VALIDATION.md for checks actually performed.

## Getting started

Use Python in a dedicated virtual environment. Install `requirements.txt` if present, otherwise inspect the imports before installing dependencies. Run an appropriate entry script, for example `python "mod6_labs/main.py"`, from its expected working directory. Interactive exercises may prompt for input.

## Contents

See [FILES.md](FILES.md) for the file inventory and [DATA.md](DATA.md) for inputs and exclusions. Original documentation, when supplied, follows below. Nonidentical drafts remain identifiable by their original names or a `variant` suffix.

## Provenance and credits

Original comments, team names and reference credits are retained. This repository represents coursework in Carl Renz Colico’s learning portfolio; collaborative or starter code is not claimed as solely individual work.

Source submissions: `cccs106-projects-main.zip`

No new blanket license is applied to third-party assets, datasets, course templates or collaborative work. Existing notices remain applicable.

## Topics

python, flet, sqlite, gui, application-development, coursework

---

## Original project documentation

# CCCS 106 Projects
Application Development and Emerging Technologies  
Academic Year 2025-2026

## Student Information
- **Name:** Carl Renz M. Colico
- **Student ID:** [STUDENT_ID_REMOVED]
- **Program:** Bachelor of Science in Computer Science
- **Section:** BSCS-3A

## Repository Structure

### Week 1 Labs - Environment Setup and Python Basics
- `week1_labs/hello_world.py` - Basic Python introduction
- `week1_labs/basic_calculator.py` - Simple console calculator
### Week 2 Labs - Git and Flet GUI Development
- `week2_labs/hello_flet.py` - First Flet GUI application
- `week2_labs/personal_info_gui.py` - Enhanced personal information manager
- `week2_labs/enhanced_calculator.py` - GUI calculator (coming soon)
### Week 3 Labs
- `week3_labs/contact_book_cli.py` - Console-based Contact Book application
### Week 4 Labs
- `week4_labs/contact_book_app/` - Console-based Contact Book application
- `main.py` - Main Flet GUI application
- `app_logic.py` - Handles adding, displaying, editing, deleting, and searching contacts
- `database.py` - SQLite database integration for persistent contact storage
###  Final Project
- `module1_final/` - Pharmacy Management System (PMS) with collab group. Project is in this link: https://github.com/frnonato-lgtm/Pharmacy-Management-System.git

## Technologies Used
- **Python 3.8+** - Main programming language
- **Flet 0.28.3** - GUI framework for cross-platform applications
- **SQLite** - GUI framework for 
- **Git & GitHub** - Version control and collaboration
- **VS Code** - Integrated development environment

## Development Environment
- **Virtual Environment:** cccs106_env
- **Python Packages:** flet==0.28.3
- **Platform:** Windows 10/11

## How to Run Applications

### Prerequisites
1. Python 3.8+ installed
2. Virtual environment activated: `cccs106_env\Scripts\activate`
3. Flet installed: `pip install flet==0.28.3`

### Running GUI Applications
```cmd
# Navigate to project directory
cd week2_labs

# Run applications
python hello_flet.py
python personal_info_gui.py
Commit and push README.md

# Add the updated README.md file to the staging area
# This stages the modified README.md file so it will be included in the next commit
# Git tracks changes to this file and prepares it for version control
git add README.md

# Commit the staged changes with a descriptive message
# Creates a permanent snapshot of the README.md updates in the repository history
# The commit message should clearly describe what was changed for future reference
git commit -m "Update README.md with new application information"

# Push the committed changes to the remote GitHub repository
# Synchronizes your local main branch with the remote repository on GitHub
# This makes your updated README.md visible to others and backs up your changes git push origin main

### Running GUI Applications Week 3
```cmd
# Navigate to project directory
cd week3_labs
# Run applications
python contact_book_cli.py

### Running GUI Applications Week 4
# Navigate to project directory
cd week4_labs/contact_book_app
# Run applications
flet run main.py


## Application preservation

Application source and dependency files match the pre-portfolio GitHub version. The introductory CCCS exercise retains a personal-ID placeholder; application logic is unchanged by that privacy substitution. Portfolio documentation, topics and ignore rules are separate additions.
