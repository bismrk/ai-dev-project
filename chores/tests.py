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

from django.contrib.auth import get_user_model
CustomUser = get_user_model()

class OnboardingViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="onboard_user", password="password123")

    def test_create_household_view(self):
        self.client.login(username="onboard_user", password="password123")
        response = self.client.post('/onboarding/', {
            'create': 'create',
            'name': 'New House'
        })
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.household)
        self.assertEqual(self.user.household.name, 'New House')
        self.assertEqual(self.user.role, 'admin')
        self.assertRedirects(response, '/') # wait, dashboard is just '/'

    def test_join_household_view(self):
        household = Household.objects.create(name="Join House")
        self.client.login(username="onboard_user", password="password123")
        response = self.client.post('/onboarding/', {
            'join': 'join',
            'join_code': household.join_code
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.household, household)
        self.assertEqual(self.user.role, 'member')
        self.assertRedirects(response, '/')

from .models import Task, DutySchedule
from datetime import date

class DashboardViewTest(TestCase):
    def setUp(self):
        self.household_a = Household.objects.create(name="House A")
        self.household_b = Household.objects.create(name="House B")
        
        self.user_a = CustomUser.objects.create_user(username="user_a", password="password123", household=self.household_a)
        self.user_b = CustomUser.objects.create_user(username="user_b", password="password123", household=self.household_b)
        
        self.schedule_a = DutySchedule.objects.create(week_start_date=date.today(), assigned_user=self.user_a, household=self.household_a)
        self.schedule_b = DutySchedule.objects.create(week_start_date=date.today(), assigned_user=self.user_b, household=self.household_b)
        
        self.task_a = Task.objects.create(title="Task A", duty_schedule=self.schedule_a, due_date=date.today(), deadline_time="18:00:00", status=False)
        self.task_b = Task.objects.create(title="Task B", duty_schedule=self.schedule_b, due_date=date.today(), deadline_time="18:00:00", status=False)

    def test_dashboard_multi_tenancy(self):
        self.client.login(username="user_a", password="password123")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task A")
        self.assertNotContains(response, "Task B")

    def test_dashboard_rendering(self):
        self.client.login(username="user_a", password="password123")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chores/dashboard.html')

from .models import SwapRequest

class DutySwapViewTest(TestCase):
    def setUp(self):
        self.household = Household.objects.create(name="Swap House")
        self.user1 = CustomUser.objects.create_user(username="swapuser1", password="password123", household=self.household)
        self.user2 = CustomUser.objects.create_user(username="swapuser2", password="password123", household=self.household)
        self.schedule = DutySchedule.objects.create(week_start_date=date.today(), assigned_user=self.user1, household=self.household)

    def test_create_swap_request(self):
        self.client.login(username="swapuser1", password="password123")
        response = self.client.post('/swaps/', {
            'action': 'request_swap',
            'schedule_id': self.schedule.id,
            'to_user_id': self.user2.id
        })
        self.assertRedirects(response, '/swaps/')
        swap = SwapRequest.objects.get(from_user=self.user1, to_user=self.user2)
        self.assertEqual(swap.status, 'pending')
        self.assertEqual(swap.target_schedule, self.schedule)

    def test_accept_swap_request(self):
        swap = SwapRequest.objects.create(from_user=self.user1, to_user=self.user2, target_schedule=self.schedule, status='pending')
        self.client.login(username="swapuser2", password="password123")
        response = self.client.post('/swaps/', {
            'action': 'accept',
            'swap_id': swap.id
        })
        self.assertRedirects(response, '/swaps/')
        swap.refresh_from_db()
        self.assertEqual(swap.status, 'accepted')
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.assigned_user, self.user2)

from unittest.mock import patch
from .utils.telegram import send_telegram_message

class TelegramUtilityTest(TestCase):
    @patch('chores.utils.telegram.requests.post')
    def test_send_telegram_message(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.raise_for_status.return_value = None
        
        with override_settings(TELEGRAM_BOT_TOKEN='fake_token'):
            result = send_telegram_message('12345', 'Hello World')
            
            self.assertTrue(result)
            mock_post.assert_called_once_with(
                'https://api.telegram.org/botfake_token/sendMessage',
                json={
                    'chat_id': '12345',
                    'text': 'Hello World',
                    'parse_mode': 'HTML'
                },
                timeout=5
            )

    @patch('chores.utils.telegram.requests.post')
    def test_send_telegram_message_no_token(self, mock_post):
        with override_settings(TELEGRAM_BOT_TOKEN=''):
            result = send_telegram_message('12345', 'Hello World')
            self.assertFalse(result)
            mock_post.assert_not_called()
