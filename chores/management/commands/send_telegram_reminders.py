from django.core.management.base import BaseCommand
from datetime import date
from chores.models import Task, DutySchedule
from chores.telegram_utils import send_telegram_message

class Command(BaseCommand):
    help = 'Sends Telegram reminders for pending tasks due today.'

    def handle(self, *args, **options):
        today = date.today()
        # Find all tasks due today that are NOT status=True
        pending_tasks = Task.objects.filter(due_date=today, status=False)
        
        # Group tasks by assigned user
        user_tasks = {}
        for task in pending_tasks:
            assigned_user = task.duty_schedule.assigned_user
            if assigned_user.telegram_chat_id:
                if assigned_user not in user_tasks:
                    user_tasks[assigned_user] = []
                user_tasks[assigned_user].append(task)
                
        if not user_tasks:
            self.stdout.write(self.style.SUCCESS("No pending tasks to notify about."))
            return
            
        for user, tasks in user_tasks.items():
            text = f"Hello {user.username}!\nYou have {len(tasks)} pending chore(s) for today:\n"
            for t in tasks:
                text += f"- {t.title} (due by {t.deadline_time.strftime('%H:%M')})\n"
            
            success = send_telegram_message(user.telegram_chat_id, text)
            if success:
                self.stdout.write(self.style.SUCCESS(f"Sent reminder to {user.username}."))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to send reminder to {user.username}."))
