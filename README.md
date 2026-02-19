# Travel Buddy AI for Solo Travellers

A lightweight AI-style travel assistant scaffold that accepts traveler inputs and generates a personalized trip strategy.

## What it does
- Takes key user inputs: **budget, duration, destination, experience style**, and extra situational preferences.
- Asks smart follow-up questions to clarify constraints (safety, remote work, pace, low budget tradeoffs).
- Generates a personalized plan with:
  - arrival transport strategy,
  - local transport strategy,
  - accommodation recommendation,
  - hidden gems,
  - day-by-day itinerary blocks,
  - booking/deals ideas,
  - actionable next-best steps.
- Supports in-trip adaptability:
  - revise plan when constraints change,
  - answer dynamic travel questions (book next train vs explore event),
  - suggest immediate in-city next moves by time of day.

## Run
```bash
python -m travel_buddy.cli
```

Then paste JSON like:

```json
{
  "budget_usd": 1400,
  "duration_days": 6,
  "destination": "Lisbon",
  "experience_type": "culture",
  "pace": "balanced",
  "food_preference": "vegetarian-friendly",
  "safety_priority": "high",
  "remote_work": false
}
```

## Notes
This repo provides a reasoning/planning engine scaffold. You can integrate an LLM + real booking APIs next (flights, rail, hotels, events, and deal providers) to make it production-ready.
