import unittest

from travel_buddy.advisor import answer_travel_question, in_city_suggestions
from travel_buddy.cli import build_profile_from_dict
from travel_buddy.planner import collect_followup_questions, generate_plan, revise_plan


class TravelBuddyTests(unittest.TestCase):
    def setUp(self):
        self.profile = build_profile_from_dict(
            {
                "budget_usd": 1200,
                "duration_days": 5,
                "destination": "Tokyo",
                "experience_type": "food",
                "pace": "fast",
                "food_preference": "omnivore",
                "safety_priority": "high",
                "remote_work": True,
            }
        )

    def test_followup_questions(self):
        qs = collect_followup_questions(self.profile)
        self.assertGreaterEqual(len(qs), 2)

    def test_plan_generation(self):
        plan = generate_plan(self.profile)
        self.assertEqual(plan.destination, "Tokyo")
        self.assertEqual(len(plan.day_by_day), 5)
        self.assertGreater(len(plan.hidden_gems), 0)

    def test_revision(self):
        plan = generate_plan(self.profile)
        revised = revise_plan(plan, {"budget_note": "reduce food spend by 20%"})
        self.assertTrue(any("Budget adjustment noted" in s for s in revised.next_best_steps))

    def test_question_answering(self):
        plan = generate_plan(self.profile)
        ans = answer_travel_question(plan, "Should I book my next train now?")
        self.assertIn("book", ans.lower())

    def test_in_city_suggestions(self):
        suggestions = in_city_suggestions("Tokyo", hour_24=20)
        self.assertTrue(any("Evening" in s for s in suggestions))


if __name__ == "__main__":
    unittest.main()
