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
