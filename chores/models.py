import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

def generate_join_code():
    return uuid.uuid4().hex[:8].upper()

class Household(models.Model):
    name = models.CharField(max_length=255)
    join_code = models.CharField(max_length=50, unique=True, default=generate_join_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    household = models.ForeignKey(Household, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def __str__(self):
        return self.username

class DutySchedule(models.Model):
    week_start_date = models.DateField()
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='duty_schedules')
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='duty_schedules')

    def __str__(self):
        return f"{self.household.name} - {self.week_start_date} ({self.assigned_user.username})"

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline_time = models.TimeField()
    due_date = models.DateField()
    status = models.BooleanField(default=False)
    duty_schedule = models.ForeignKey(DutySchedule, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f"{self.title} - {self.due_date}"

class SwapRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_swap_requests')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_swap_requests')
    target_schedule = models.ForeignKey(DutySchedule, on_delete=models.CASCADE, related_name='swap_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Swap {self.from_user} -> {self.to_user} for {self.target_schedule}"
