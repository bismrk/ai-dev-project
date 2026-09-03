# Product Backlog: Shared Household Chores Tracker

## 1. Project Initialization & Testing
Goal: Set up an empty Django project with a passing test.
Description: Initialize the Python virtual environment and install Django. Create the basic `config` project and `chores` app, and write a simple dummy test to ensure the test runner works.

## 2. Household Model
Goal: Implement the Household model to support multiple apartments/families.
Description: Create a `Household` model with a `name` and a unique `join_code`. This will act as the core tenant model to isolate data between different groups of roommates or families.

## 3. User Model & Authentication Setup
Goal: Implement the CustomUser model with Telegram chat ID and Household link.
Description: Extend Django's AbstractUser to create a `CustomUser` model that includes a `telegram_chat_id`, a `role` (Admin/Member), and a foreign key to the `Household` model. Configure the Django settings to use this new user model.

## 4. Duty Schedule Data Model
Goal: Create the DutySchedule model to track weekly chore assignments.
Description: Define the `DutySchedule` model with fields for the week's start date, a foreign key to the `CustomUser` assigned, and a foreign key to the `Household`. Register this model in the Django admin panel.

## 5. Task Data Model
Goal: Implement the Task model for individual chores.
Description: Create the `Task` model containing the title, description, deadline time, due date, and a boolean status field. Link this model via a foreign key to the `DutySchedule`, and register it in the admin.

## 6. Swap Request Data Model
Goal: Build the SwapRequest model to handle duty exchange logic.
Description: Create the `SwapRequest` model with foreign keys for the requesting user, the receiving user, and the target `DutySchedule`. Include a status field (pending, accepted, rejected) and register it in the admin.

## 7. Frontend: Base Layout & Styling System
Goal: Create a premium, responsive base HTML template using Vanilla CSS.
Description: Set up Django's static files and template directories. Create a `base.html` template that includes modern Vanilla CSS (using CSS variables, Grid, and Flexbox) to serve as the foundation for all pages.

## 8. Frontend: Household Onboarding
Goal: Build views for creating or joining a Household.
Description: Create pages allowing a new user to either create a new Household (becoming its Admin) or join an existing one using a `join_code`.

## 9. Frontend: Resident Dashboard
Goal: Build the main dashboard view to display current chores for the household.
Description: Create a Django view and template for the dashboard. It should query the database for today's active tasks based on the current `DutySchedule` of the user's `Household`, and display them in "To Do" and "Done" visual columns.

## 10. Frontend: Duty Swap Interface
Goal: Implement the views and templates for requesting and managing swaps.
Description: Build a dedicated page where users can view the upcoming duty roster for their household and submit a swap request to another household member. Include logic for accepting or rejecting a swap.

## 11. Telegram Notification Utility
Goal: Create a utility function to send messages via the Telegram API.
Description: Implement a Python module using the `requests` library that takes a Telegram chat ID and a message string. Use a bot token from Django settings to securely send HTTP POST requests to the Telegram Bot API.

## 12. Background Cron Command
Goal: Write a custom Django management command to trigger reminders.
Description: Create a management command `send_telegram_reminders` that queries the database for incomplete tasks due today across all households. For any found, it looks up the assigned user's Telegram ID via the `DutySchedule` and sends them a notification.
