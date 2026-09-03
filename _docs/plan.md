# Specification: Shared Household Chores Tracker

## 1. Project Overview
A web-based application designed to help people who rent an apartment together (roommates) and large families (3 or more people) manage and distribute household chores. The system operates on a weekly rotation basis where one person is assigned as the "Duty Person". This person is responsible for a predefined list of tasks with strict deadlines. The application includes a swapping mechanism for flexibility, supports multiple isolated households, and integrates with Telegram to send automated reminders.

## 2. Core Features
1. **Multi-Household Support:**
   - Users are grouped into isolated "Households" (representing an apartment of roommates or a family).
   - All tasks, schedules, and members are scoped to the specific household.
2. **Weekly Duty Roster & Swaps:** 
   - Automated or manual assignment of a "Duty Person" for the current week within the household.
   - **Swap Requests:** If the assigned person is unavailable, they can send a swap request to another household member. If accepted, their duty weeks are exchanged.
3. **Task Management & Hard Deadlines:** 
   - Ability to create tasks (e.g., "Clean the floors", "Take out the trash").
   - Each task is bound to a specific hard deadline (e.g., "by 12:00 PM", "by 8:00 PM").
   - A visual board to track the status of current tasks (To Do, Done).
4. **Telegram Notification System:**
   - A background process that checks the status of the daily tasks.
   - Sends automated alerts to the current Duty Person via Telegram every 3 hours containing a list of pending tasks that must be completed today.

## 3. User Roles
- **Household Admin:** (e.g., Parent or Main Tenant) Can create the household, invite members, add/remove residents, and define the master list of weekly tasks.
- **Resident / Family Member (User):** Can view the board, complete tasks, request duty swaps, and accept/reject swap requests.

## 4. User Stories
- *As a Resident/Family Member, I want to join my specific household so that I only see my roommates/family.*
- *As a Resident, I want to see whose turn it is to do chores this week, so I know who is responsible.*
- *As a Duty Person, I want to see a clear list of my tasks and their deadlines, so I can plan my day.*
- *As a Duty Person, I want to receive Telegram reminders every 3 hours for unfinished tasks, so I don't forget my responsibilities.*
- *As a Resident, I want to request a duty swap with my roommate/sibling if I am unavailable, so the house still gets cleaned.*

## 5. High-Level Data Model
- **Household:** name, join_code (to invite members).
- **User:** name, telegram_chat_id, household_id, role (admin/member).
- **Task:** title, description, deadline_time, status (pending/completed), household_id.
- **DutySchedule:** week_start_date, assigned_user, household_id.
- **SwapRequest:** from_user, to_user, target_week, status.

## 6. Out of Scope for MVP (Minimum Viable Product)
- Managing shared expenses or grocery bills.
- Complex gamification (points, leaderboards).
- Mobile application (we will focus on a responsive web app first).
