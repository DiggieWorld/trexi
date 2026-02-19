from __future__ import annotations

from dataclasses import replace
from math import ceil
from typing import Dict, List

from .models import DayPlan, PlanItem, TravelPlan, TravelerProfile


EXPERIENCE_FOCUS = {
    "adventure": ["hiking route", "outdoor activity", "local market"],
    "culture": ["museum", "heritage walk", "live performance"],
    "food": ["street food trail", "cooking class", "night food district"],
    "relax": ["park / waterfront", "wellness stop", "sunset viewpoint"],
}

HIDDEN_GEMS: Dict[str, List[str]] = {
    "tokyo": ["Yanaka Ginza alley", "Kagurazaka side streets", "Shimokitazawa vinyl cafes"],
    "lisbon": ["Jardim do Torel", "LX Factory back galleries", "Miradouro da Senhora do Monte at sunrise"],
    "bangkok": ["Talad Noi street art lane", "Bang Krachao cycling loop", "Artist's House at Khlong Bang Luang"],
}

DEALS: Dict[str, List[str]] = {
    "tokyo": ["72-hour metro pass bundle", "Early-bird Shinkansen regional discount"],
    "lisbon": ["Lisboa Card + airport transfer combo", "Sintra roundtrip off-peak fare"],
    "bangkok": ["BTS Rabbit card starter discount", "Island ferry weekday promo"],
}


def collect_followup_questions(profile: TravelerProfile) -> List[str]:
    questions: List[str] = []
    if profile.safety_priority.lower() in {"high", "very high"}:
        questions.append("Do you prefer accommodations with 24/7 reception and well-lit surroundings?")
    if profile.remote_work:
        questions.append("How many hours per day do you need stable Wi-Fi for work calls?")
    if profile.pace.lower() == "fast":
        questions.append("Would you like 1 flexible buffer slot per day in case of delays?")
    if profile.budget_usd < 800:
        questions.append("Are overnight buses/trains acceptable to reduce accommodation costs?")
    return questions


def _allocate_budget(profile: TravelerProfile) -> Dict[str, int]:
    destination_transport = ceil(profile.budget_usd * 0.20)
    stay = ceil(profile.budget_usd * 0.45)
    local = ceil(profile.budget_usd * 0.15)
    activities = profile.budget_usd - destination_transport - stay - local
    return {
        "destination_transport": destination_transport,
        "stay": stay,
        "local": local,
        "activities": activities,
    }


def _transport_recommendation(profile: TravelerProfile, budget: Dict[str, int]) -> PlanItem:
    if profile.duration_days <= 4:
        title = "Fastest route"
        detail = f"Book a direct flight to {profile.destination} with cabin baggage only to save transfer time."
    elif budget["destination_transport"] < 250:
        title = "Budget route"
        detail = f"Use low-cost carrier + public airport transfer in {profile.destination}."
    else:
        title = "Balanced route"
        detail = f"Book mid-tier flight/train with free cancellation and arrive before noon for easier check-in."
    return PlanItem(title=title, detail=detail, estimated_cost_usd=budget["destination_transport"])


def _local_transport(profile: TravelerProfile, budget: Dict[str, int]) -> PlanItem:
    detail = (
        "Use a reloadable city transit pass for metro/bus, and keep one ride-share app as backup for late nights."
    )
    if profile.pace.lower() == "slow":
        detail += " Include walking circuits between nearby attractions to reduce daily transfer stress."
    return PlanItem(title="City mobility", detail=detail, estimated_cost_usd=budget["local"])


def _accommodation(profile: TravelerProfile, budget: Dict[str, int]) -> PlanItem:
    if profile.safety_priority.lower() in {"high", "very high"}:
        title = "Safe central stay"
        detail = "Choose a highly rated hostel/private room near a major transit hub with late check-in support."
    elif profile.budget_usd > 1800:
        title = "Comfort stay"
        detail = "Book a boutique hotel with breakfast and free cancellation for itinerary flexibility."
    else:
        title = "Value stay"
        detail = "Pick a co-living hostel or budget hotel with lockers and positive solo traveler reviews."
    return PlanItem(title=title, detail=detail, estimated_cost_usd=budget["stay"])


def _build_day_plans(profile: TravelerProfile, activity_budget: int) -> List[DayPlan]:
    focus = EXPERIENCE_FOCUS.get(profile.experience_type.lower(), EXPERIENCE_FOCUS["culture"])
    per_day = max(20, activity_budget // max(profile.duration_days, 1))
    plans = []
    for i in range(1, profile.duration_days + 1):
        plans.append(
            DayPlan(
                day=i,
                morning=f"{focus[0].title()} + cafe planning hour (budget ~${per_day//3})",
                afternoon=f"{focus[1].title()} and local lunch (budget ~${per_day//3})",
                evening=f"{focus[2].title()} with social/community option (budget ~${per_day//3})",
                focus=profile.experience_type,
            )
        )
    return plans


def generate_plan(profile: TravelerProfile) -> TravelPlan:
    budget = _allocate_budget(profile)
    destination_key = profile.destination.strip().lower()

    plan = TravelPlan(
        destination=profile.destination,
        transport_to_destination=_transport_recommendation(profile, budget),
        local_transport=_local_transport(profile, budget),
        accommodation=_accommodation(profile, budget),
        hidden_gems=HIDDEN_GEMS.get(destination_key, ["Ask locals for neighborhood events 24h in advance"]),
        day_by_day=_build_day_plans(profile, budget["activities"]),
        booking_deals=DEALS.get(destination_key, ["Set fare alert and monitor 3 booking sites for flash discounts"]),
        next_best_steps=[
            "Confirm arrival transfer and first-night check-in before departure.",
            "Book only first 40% of activities now; keep room for local discoveries.",
            "Enable weather alerts and transport delay notifications.",
        ],
    )
    return plan


def revise_plan(plan: TravelPlan, changes: Dict[str, str]) -> TravelPlan:
    updated = plan
    if "destination" in changes:
        updated = replace(updated, destination=changes["destination"])
    if "budget_note" in changes:
        updated.next_best_steps.append(f"Budget adjustment noted: {changes['budget_note']}")
    if "interest" in changes:
        updated.next_best_steps.append(f"Add this to tomorrow: {changes['interest']}")
    return updated
