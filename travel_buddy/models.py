from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class TravelerProfile:
    budget_usd: int
    duration_days: int
    destination: str
    experience_type: str
    pace: str
    food_preference: str
    safety_priority: str
    remote_work: bool = False


@dataclass
class PlanItem:
    title: str
    detail: str
    estimated_cost_usd: int


@dataclass
class DayPlan:
    day: int
    morning: str
    afternoon: str
    evening: str
    focus: str


@dataclass
class TravelPlan:
    destination: str
    transport_to_destination: PlanItem
    local_transport: PlanItem
    accommodation: PlanItem
    hidden_gems: List[str] = field(default_factory=list)
    day_by_day: List[DayPlan] = field(default_factory=list)
    booking_deals: List[str] = field(default_factory=list)
    next_best_steps: List[str] = field(default_factory=list)
