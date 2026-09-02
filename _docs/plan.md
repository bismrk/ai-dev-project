# Specification: Shared Household Chores Tracker

## 1. Project Overview
A web-based application designed to help roommates or family members manage and distribute household chores. The system operates on a weekly rotation basis where one person is assigned as the "Duty Person". This person is responsible for a predefined list of tasks with strict deadlines. The application includes a swapping mechanism for flexibility and integrates with Telegram to send automated reminders.

## 2. Core Features
1. **Weekly Duty Roster & Swaps:** 
   - Automated or manual assignment of a "Duty Person" for the current week.
   - **Swap Requests:** If the assigned person is unavailable, they can send a swap request to another member. If accepted, their duty weeks are exchanged.
2. **Task Management & Hard Deadlines:** 
   - Ability to create tasks (e.g., "Clean the floors", "Take out the trash").
   - Each task is bound to a specific hard deadline (e.g., "by 12:00 PM", "by 8:00 PM").
   - A visual board to track the status of current tasks (To Do, Done).
3. **Telegram Notification System:**
   - A background process that checks the status of the daily tasks.
   - Sends automated alerts to the current Duty Person via Telegram every 3 hours containing a list of pending tasks that must be completed today.

## 3. User Roles
- **Resident (User):** Can view the board, complete tasks, request duty swaps, and accept/reject swap requests.
- **Admin (Optional for v1):** Can manage the household, add/remove residents, and define the master list of weekly tasks.

## 4. User Stories
- *As a Resident, I want to see whose turn it is to do chores this week, so I know who is responsible.*
- *As a Duty Person, I want to see a clear list of my tasks and their deadlines, so I can plan my day.*
- *As a Duty Person, I want to receive Telegram reminders every 3 hours for unfinished tasks, so I don't forget my responsibilities.*
- *As a Resident, I want to request a duty swap with my roommate if I am out of town, so the house still gets cleaned.*

## 5. High-Level Data Model
- **User:** name, telegram_chat_id (for notifications).
- **Task:** title, description, deadline_time, status (pending/completed).
- **DutySchedule:** week_start_date, assigned_user.
- **SwapRequest:** from_user, to_user, target_week, status (pending/accepted/rejected).

## 6. Out of Scope for MVP (Minimum Viable Product)
- Managing shared expenses or grocery bills.
- Complex gamification (points, leaderboards).
- Mobile application (we will focus on a responsive web app first).
