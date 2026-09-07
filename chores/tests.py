from django.test import TestCase
from .models import Household

class HouseholdModelTest(TestCase):
    def test_household_creation(self):
        household = Household.objects.create(name="Test House")
        self.assertEqual(household.name, "Test House")
        self.assertIsNotNone(household.join_code)
        self.assertTrue(len(household.join_code) > 0)
        
    def test_unique_join_code(self):
        h1 = Household.objects.create(name="House 1")
        h2 = Household.objects.create(name="House 2")
        self.assertNotEqual(h1.join_code, h2.join_code)

    def test_unique_constraint(self):
        from django.db import IntegrityError
        Household.objects.create(name="House 1", join_code="SAMECODE")
        with self.assertRaises(IntegrityError):
            Household.objects.create(name="House 2", join_code="SAMECODE")

    def test_string_representation(self):
        household = Household.objects.create(name="House 1")
        self.assertEqual(str(household), "House 1")

from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username="testuser", password="password123", role="member")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "member")

    def test_foreign_key(self):
        household = Household.objects.create(name="User House")
        user = User.objects.create_user(username="memberuser", password="password123", household=household)
        self.assertEqual(user.household.name, "User House")
        self.assertIn(user, household.members.all())

from .models import DutySchedule
from datetime import date
from django.db import IntegrityError

class DutyScheduleModelTest(TestCase):
    def setUp(self):
        self.household = Household.objects.create(name="Schedule House")
        self.user = User.objects.create_user(username="scheduser", password="123", household=self.household)

    def test_schedule_creation(self):
        schedule = DutySchedule.objects.create(
            week_start_date=date(2023, 1, 1),
            assigned_user=self.user,
            household=self.household
        )
        self.assertEqual(schedule.assigned_user.username, "scheduser")

    def test_unique_constraint(self):
        DutySchedule.objects.create(
            week_start_date=date(2023, 1, 1),
            assigned_user=self.user,
            household=self.household
        )
        with self.assertRaises(IntegrityError):
            DutySchedule.objects.create(
                week_start_date=date(2023, 1, 1),
                assigned_user=self.user,
                household=self.household
            )

    def test_string_representation(self):
        schedule = DutySchedule.objects.create(
            week_start_date=date(2023, 1, 1),
            assigned_user=self.user,
            household=self.household
        )
        self.assertEqual(str(schedule), "Schedule House - Week of 2023-01-01")

from .models import Task
from datetime import time

class TaskModelTest(TestCase):
    def setUp(self):
        self.household = Household.objects.create(name="Task House")
        self.user = User.objects.create_user(username="taskuser", password="123", household=self.household)
        self.schedule = DutySchedule.objects.create(
            week_start_date=date(2023, 1, 1),
            assigned_user=self.user,
            household=self.household
        )

    def test_task_creation_and_defaults(self):
        task = Task.objects.create(
            title="Clean Kitchen",
            deadline_time=time(12, 0),
            due_date=date(2023, 1, 2),
            duty_schedule=self.schedule
        )
        self.assertEqual(task.title, "Clean Kitchen")
        self.assertFalse(task.status)
        self.assertEqual(str(task), "Clean Kitchen")

from .models import SwapRequest

class SwapRequestModelTest(TestCase):
    def setUp(self):
        self.household = Household.objects.create(name="Swap House")
        self.user1 = User.objects.create_user(username="swap1", password="123", household=self.household)
        self.user2 = User.objects.create_user(username="swap2", password="123", household=self.household)
        self.schedule = DutySchedule.objects.create(
            week_start_date=date(2023, 1, 1),
            assigned_user=self.user1,
            household=self.household
        )

    def test_swap_request_creation_and_defaults(self):
        swap = SwapRequest.objects.create(
            from_user=self.user1,
            to_user=self.user2,
            target_schedule=self.schedule
        )
        self.assertEqual(swap.from_user.username, "swap1")
        self.assertEqual(swap.status, "pending")

from django.urls import path
from django.shortcuts import render
from django.test import override_settings

def dummy_base_view(request):
    return render(request, 'base.html')

urlpatterns = [
    path('test-base/', dummy_base_view),
]

@override_settings(ROOT_URLCONF=__name__)
class FrontendBaseLayoutTest(TestCase):
    def test_base_html_renders(self):
        response = self.client.get('/test-base/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<html lang="en">')
        self.assertContains(response, 'css/style.css')
