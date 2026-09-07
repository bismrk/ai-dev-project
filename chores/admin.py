from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Household, CustomUser, DutySchedule, Task, SwapRequest

@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('name', 'join_code', 'created_at')
    search_fields = ('name', 'join_code')
    readonly_fields = ('join_code', 'created_at')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'household', 'role')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('telegram_chat_id', 'role', 'household')}),
    )

@admin.register(DutySchedule)
class DutyScheduleAdmin(admin.ModelAdmin):
    list_display = ('household', 'week_start_date', 'assigned_user')
    list_filter = ('household', 'week_start_date')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'deadline_time', 'status', 'duty_schedule')
    list_filter = ('status', 'due_date')

@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'target_schedule', 'status', 'created_at')
    list_filter = ('status',)
