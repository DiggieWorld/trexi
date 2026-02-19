from __future__ import annotations

import json

from .advisor import answer_travel_question, in_city_suggestions
from .models import TravelerProfile
from .planner import collect_followup_questions, generate_plan, revise_plan


def build_profile_from_dict(raw: dict) -> TravelerProfile:
    return TravelerProfile(
        budget_usd=int(raw["budget_usd"]),
        duration_days=int(raw["duration_days"]),
        destination=raw["destination"],
        experience_type=raw["experience_type"],
        pace=raw.get("pace", "balanced"),
        food_preference=raw.get("food_preference", "no preference"),
        safety_priority=raw.get("safety_priority", "medium"),
        remote_work=bool(raw.get("remote_work", False)),
    )


def run_cli() -> None:
    print("Travel Buddy AI - Enter JSON input:")
    raw = json.loads(input().strip())
    profile = build_profile_from_dict(raw)

    followups = collect_followup_questions(profile)
    if followups:
        print("Follow-up questions:")
        for q in followups:
            print(f"- {q}")

    plan = generate_plan(profile)
    print("\n=== Personalized Plan ===")
    print(f"Destination: {plan.destination}")
    print(f"Transport: {plan.transport_to_destination.detail}")
    print(f"Local transport: {plan.local_transport.detail}")
    print(f"Accommodation: {plan.accommodation.detail}")
    print("Hidden gems:")
    for gem in plan.hidden_gems:
        print(f"- {gem}")

    print("\nAsk one travel question:")
    q = input().strip()
    print(answer_travel_question(plan, q))

    print("\nIn-city suggestions:")
    for s in in_city_suggestions(plan.destination):
        print(f"- {s}")

    print("\nOptional updates as JSON (or blank):")
    update = input().strip()
    if update:
        plan = revise_plan(plan, json.loads(update))
        print("Updated next steps:")
        for step in plan.next_best_steps:
            print(f"- {step}")


if __name__ == "__main__":
    run_cli()
