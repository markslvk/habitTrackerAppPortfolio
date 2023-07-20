import unittest
from datetime import date, datetime, timedelta
from habitClass import Habit
from timerClass import Timer
import io
import sys


class HabitTests(unittest.TestCase):

    def setUp(self):
        #set up any necessary objects or variables for the tests
        self.habit = Habit("Test Habit", "daily", "This is a test habit")
        self.timer = Timer("daily")

    def tearDown(self):
        #clean up any resources used by the tests
        self.habit = None
        self.timer = None

    def test_habit_creation(self):
        #test if the habit is created correctly
        expected_creation_date = datetime.strptime('2023-07-18 11:14:42', '%Y-%m-%d %H:%M:%S').date()
        self.assertEqual(self.habit.creation_date, expected_creation_date)
        self.assertEqual(self.habit.name, "Test Habit")
        self.assertEqual(self.habit.periodicity, "daily")
        self.assertEqual(self.habit.description, "This is a test habit")
        self.assertEqual(self.habit.streak, 0)
        self.assertEqual(self.habit.log_num, 0)
        self.assertEqual(self.habit.check_log, [])
        self.assertFalse(self.habit.time_done)
        self.assertFalse(self.habit.did)

    def test_habit_update_streak(self):
        #test the update_streak method of the Habit classs
        self.habit.did = True
        self.habit.update_streak()
        self.assertEqual(self.habit.streak, 1)
        self.assertEqual(self.habit.highest_streak, 1)

        self.habit.did = False
        self.habit.update_streak()
        self.assertEqual(self.habit.streak, 0)
        self.assertEqual(self.habit.highest_streak, 1)
        self.assertEqual(self.habit.difficulty_count, 1)

    def test_timer_time_lapse(self):
        #test the time_lapse method of the Timer class
        expected_due_date = datetime.now() + timedelta(days=1)
        actual_due_date = self.timer.time_lapse()
        self.assertEqual(actual_due_date.date(), expected_due_date.date())
        
    def test_habit_timeout(self):
        self.habit.timeout()
        self.assertFalse(self.habit.did)
        self.assertFalse(self.habit.time_done)
        self.assertEqual(self.habit.due_date.date(), (datetime.now() + timedelta(days=1)).date())



if __name__ == "__main__":
    unittest.main()