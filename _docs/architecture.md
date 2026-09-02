# Architecture: Shared Household Chores Tracker

This document outlines the high-level architecture and data models for our Django-based application.

## High-Level Architecture

Our app follows a classic monolithic MVC (Model-View-Controller, or MTV in Django terms) pattern. Background tasks for Telegram notifications are handled by a standalone cron job running a custom Django management command.

```mermaid
graph TD
    User([User (Roommate)])
    Admin([Admin])
    Telegram([Telegram API])
    
    subgraph Django Application
        Views[Django Views & Templates]
        Models[Django ORM (Models)]
        Command[Django Management Command]
    end
    
    Cron((System Cron))
    DB[(SQLite/PostgreSQL)]

    User -->|HTTP GET/POST| Views
    Admin -->|HTTP GET/POST (Admin Panel)| Views
    
    Views <-->|Read/Write| Models
    Models <-->|Queries| DB
    
    Cron -->|Every 3 Hours| Command
    Command -->|Read| Models
    Command -->|Send| Telegram
    Telegram -.->|Notifications| User
```

## Technical Stack & Versions

- **Python:** `v3.14+`
- **Web Framework:** `Django v6.1`
- **Background Scheduler:** `System Cron` (Linux/macOS) invoking a custom Django management command.
- **HTTP Client:** `requests v2.34.2`
- **Database:** `SQLite` (built-in, development/MVP) / `PostgreSQL` (production)
- **Frontend / Styling:** Vanilla HTML/CSS with modern native web features (Grid, Flexbox, custom properties).

## Data Models

The core entities revolve around tracking users, schedules, specific tasks, and swap requests. 

```mermaid
erDiagram
    CustomUser {
        int id
        string username
        string email
        string telegram_chat_id
    }
    
    DutySchedule {
        int id
        date week_start_date
        int assigned_user_id FK
    }

    Task {
        int id
        string title
        string description
        time deadline_time
        date due_date
        boolean status
        int duty_schedule_id FK
    }

    SwapRequest {
        int id
        int from_user_id FK
        int to_user_id FK
        int target_schedule_id FK
        string status
    }

    CustomUser ||--o{ DutySchedule : "assigned to"
    DutySchedule ||--o{ Task : "contains tasks"
    CustomUser ||--o{ SwapRequest : "requests/receives"
    DutySchedule ||--o{ SwapRequest : "target of"
```

## Component Breakdown

1. **Frontend (Django Templates):**
   - Server-side rendered HTML using Django's templating engine.
   - Styled with modern Vanilla CSS for a premium look.
   - Core pages: Dashboard (current tasks), Schedule & Swaps, Admin Panel.

2. **Database:**
   - **SQLite** for development and MVP. Easily upgradeable to **PostgreSQL** in the future.
   - Django ORM handles all database interactions.

3. **Background Notification System:**
   - **System Cron**: Instead of embedding the scheduler inside the web process (which causes issues with multiple workers like Gunicorn), we will write a custom Django management command (`python manage.py send_telegram_reminders`).
   - The OS `cron` will trigger this command every 3 hours.
   - The command queries the `Task` model for incomplete tasks due today, looks up the current `DutySchedule`, and sends a message to the `assigned_user`'s Telegram via the `requests` library.
