# Antigravity Rules and Customizations

## Commands

- `.\venv\Scripts\pip install -r requirements.txt` - install dependencies
- `.\venv\Scripts\python manage.py test` - run the whole test suite
- `.\venv\Scripts\python manage.py test chores` - run tests for a specific app

## Rules

- Dependencies are added in `requirements.txt` (and installed via `pip`). Do not add one without asking the user.
- Always use the virtual environment (`.\venv\Scripts\python` or `.\venv\Scripts\pip`) for running commands.
