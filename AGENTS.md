# Antigravity Rules and Customizations

## Project Context
We are building a **Shared Household Chores Tracker** (Django web app for roommates/families).
Before starting any new task, or if you need to understand the architecture, ALWAYS read:

## Documents:
- **Spec & Architecture:** `_docs/plan.md`
- **Current Tasks:** `backlog.md`

## Commands

- `.\venv\Scripts\pip install -r requirements.txt` - Install dependencies
- `.\venv\Scripts\python manage.py runserver` - Start the local development server
- `.\venv\Scripts\python manage.py makemigrations` - Create database migrations
- `.\venv\Scripts\python manage.py migrate` - Apply database migrations
- `.\venv\Scripts\python manage.py test` - Run the whole test suite
- `.\venv\Scripts\python manage.py test chores` - Run tests for a specific app
- `.\venv\Scripts\python manage.py send_telegram_reminders` - Run the background cron job locally (when implemented)

## Rules

### 1. General & Dependencies
- Dependencies are added in `requirements.txt` (and installed via `pip`). Do not add one without asking the user.
- Always use the virtual environment (`.\venv\Scripts\python` or `.\venv\Scripts\pip`) for running commands.
- Do not remove or modify existing comments in the codebase unless explicitly requested.

### 2. Multi-Tenancy & Security (CRITICAL)
- **Data Isolation:** All database queries and views MUST filter data by the user's `Household` (e.g., `Task.objects.filter(duty_schedule__household=request.user.household)`). NEVER expose data from other households.
- **Custom User:** Ensure `AUTH_USER_MODEL` is strictly used everywhere instead of importing the default Django `User`.

### 3. Frontend & Styling
- Use **Vanilla CSS** with CSS Variables, Flexbox, and Grid for a premium, clean look.
- DO NOT use TailwindCSS, Bootstrap, or other heavy CSS frameworks unless the user explicitly asks for them.
- Ensure the design is responsive and looks good on mobile devices.

### 4. Architecture Constraints
- **Scheduler:** Do not use Celery or Redis for the MVP. Rely on the custom Django management command for Telegram notifications.
- **Task Assignment:** Remember that `Task` is linked to `DutySchedule`, NOT directly to the `User`.
