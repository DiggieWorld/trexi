from __future__ import annotations

from datetime import datetime
from typing import List

from .models import TravelPlan

EVENT_HINTS = {
    "tokyo": ["Check Koenji for indie gigs tomorrow night", "Look for weekend flea markets near Yoyogi"],
    "lisbon": ["Explore Fado houses with same-day tickets", "Watch for sunset miradouro jam sessions"],
    "bangkok": ["Check riverside live music bars", "Look for temple fair schedules in district calendars"],
}


def in_city_suggestions(city: str, hour_24: int | None = None) -> List[str]:
    now_hour = hour_24 if hour_24 is not None else datetime.now().hour
    city_key = city.strip().lower()
    suggestions: List[str] = []

    if now_hour < 12:
        suggestions.append("Morning window: reserve intercity train/bus now before dynamic fares increase.")
    elif now_hour < 18:
        suggestions.append("Afternoon window: explore one nearby neighborhood and keep evening unplanned for events.")
    else:
        suggestions.append("Evening window: decide between booking next transport or attending a local event based on energy levels.")

    suggestions.extend(EVENT_HINTS.get(city_key, ["Open local events app and filter by walking distance + today/tomorrow."]))
    suggestions.append("Re-check weather and commute time before locking tomorrow morning plans.")
    return suggestions


def answer_travel_question(plan: TravelPlan, question: str) -> str:
    q = question.lower()
    if "train" in q or "bus" in q:
        return (
            "If your next city has limited departures, book now with flexible fare; "
            "otherwise wait until after tonight's exploration to keep flexibility."
        )
    if "festival" in q or "music" in q or "event" in q:
        return (
            "Pick events within 30 minutes of your stay, then keep a transport backup for late return. "
            "Use your plan's evening slot as a swap-in."
        )
    if "budget" in q:
        return (
            f"Your current plan allocates accommodation at about ${plan.accommodation.estimated_cost_usd} and "
            f"local transport at about ${plan.local_transport.estimated_cost_usd}; adjust activity spending first."
        )
    return "I recommend choosing the option that is reversible first: refundable booking, then commit once local conditions are clear."
