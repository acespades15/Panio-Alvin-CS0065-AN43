"""TA4: illustrative weather knowledge, rules, and a complete CBR cycle.

Python 3.10+, standard library only. No live weather or personal records.
Run: python ta4_weather_reasoning.py
Use --interactive to revise the retrieved solution yourself.
Use --case-file learned_cases.json to save learning across runs.
"""

import argparse
import json
from copy import deepcopy
from pathlib import Path


# Five facts, grouped explicitly into three knowledge categories.
FACTS = {
    "atmosphere": {"temperature_c": 32, "humidity_pct": 85},
    "weather": {"is_raining": True},
    "activity": {"is_outdoors": True, "has_umbrella": False},
}
WEIGHTS = dict(temperature_c=0.25, humidity_pct=0.15,
               is_raining=0.25, is_outdoors=0.20, has_umbrella=0.15)
RANGES = {"temperature_c": (-10, 50), "humidity_pct": (0, 100)}
SEED_CASES = [
    {"id": "C1", "problem": dict(temperature_c=34, humidity_pct=55,
     is_raining=False, is_outdoors=True, has_umbrella=False),
     "solution": "Use shade and bring drinking water."},
    {"id": "C2", "problem": dict(temperature_c=28, humidity_pct=90,
     is_raining=True, is_outdoors=True, has_umbrella=False),
     "solution": "Bring an umbrella; use indoor shelter until rain eases."},
    {"id": "C3", "problem": dict(temperature_c=24, humidity_pct=60,
     is_raining=False, is_outdoors=False, has_umbrella=True),
     "solution": "Continue indoor activity; no extra weather action needed."},
]


def flatten(facts):
    """Expose the three categories as five comparable feature values."""
    features = {key: value for group in facts.values()
                for key, value in group.items()}
    validate(features)
    return features


def validate(features):
    """Reject missing, extra, mistyped, or out-of-range feature values."""
    if set(features) != set(WEIGHTS):
        raise ValueError("Exactly the five declared features are required.")
    for key, value in features.items():
        if key in RANGES:
            low, high = RANGES[key]
            if type(value) not in (int, float) or not low <= value <= high:
                raise ValueError(f"{key} must be a number in [{low}, {high}].")
        elif type(value) is not bool:
            raise ValueError(f"{key} must be True or False.")


def rule_hot(f):
    if f["temperature_c"] > 30:
        return "Move to a cooler place or turn on a fan."


def rule_rain(f):
    if f["is_raining"] and f["is_outdoors"] and not f["has_umbrella"]:
        return "Bring an umbrella."


def rule_humid(f):
    if f["humidity_pct"] >= 80:
        return "Improve ventilation where practical."


def rule_water(f):
    if f["is_outdoors"] and f["temperature_c"] >= 30:
        return "Bring drinking water."


RULES = [rule_hot, rule_rain, rule_humid, rule_water]


def infer(features):
    """A single forward pass is enough: actions do not create new facts."""
    validate(features)
    actions, trace = [], []
    for rule in RULES:
        action = rule(features)
        trace.append((rule.__name__, action is not None))
        if action and action not in actions:
            actions.append(action)
    return actions, trace


def similarity(query, problem):
    """Weighted mean of normalized numeric and exact Boolean matches."""
    validate(query)
    validate(problem)
    total = 0.0
    for key, weight in WEIGHTS.items():
        if key in RANGES:
            low, high = RANGES[key]
            score = 1 - abs(query[key] - problem[key]) / (high - low)
        else:
            score = float(query[key] == problem[key])
        total += weight * score
    return total / sum(WEIGHTS.values())


def retrieve(query, cases):
    """Return all ranked cases; insertion order breaks equal-score ties."""
    if not cases:
        raise ValueError("Cannot retrieve from an empty case base.")
    return sorted(((similarity(query, c["problem"]), c) for c in cases),
                  key=lambda pair: pair[0], reverse=True)


def revise(solution, manual_revision=""):
    """An empty revision explicitly keeps the retrieved solution."""
    return manual_revision.strip() or solution


def retain(query, solution, cases):
    """Store the revised experience without aliasing the query object."""
    validate(query)
    if not solution.strip():
        raise ValueError("A retained solution must not be empty.")
    used = {case["id"] for case in cases}
    number = 1
    while f"C{number}" in used:
        number += 1
    new_case = {"id": f"C{number}", "problem": deepcopy(query),
                "solution": solution.strip()}
    cases.append(new_case)
    return new_case


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["all", "rbr", "cbr"], default="all")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--revision", default="")
    parser.add_argument("--case-file", type=Path)
    args = parser.parse_args()
    features = flatten(FACTS)
    print("TA4 WEATHER REASONING | Illustrative educational data")
    print("INPUT: five facts in three categories")
    print(json.dumps(FACTS, indent=2))
    if args.mode in ("all", "rbr"):
        actions, trace = infer(features)
        print("\nRBR PROCESS: check every IF-THEN rule")
        for name, fired in trace:
            print(f"{name}: {'FIRED' if fired else 'not fired'}")
        print("Rule-Based Reasoning Actions:")
        for action in actions:
            print("-", action)
        if not actions:
            print("- No rule matched; no action inferred.")
    if args.mode in ("all", "cbr"):
        cases = deepcopy(SEED_CASES)
        if args.case_file and args.case_file.exists():
            cases = json.loads(args.case_file.read_text(encoding="utf-8"))
        ranked = retrieve(features, cases)
        print("\nCBR PROCESS: Retrieve -> Reuse -> Revise -> Retain")
        for score, case in ranked:
            print(f"Retrieve {case['id']}: similarity={score:.4f}")
        score, chosen = ranked[0]
        solution = chosen["solution"]  # Reuse the best matching experience.
        print(f"Reuse {chosen['id']}: {solution}")
        revision = args.revision
        if args.interactive:
            revision = input("Revised solution (Enter keeps it unchanged): ")
        solution = revise(solution, revision)
        print("Revise:", solution)
        before = len(cases)
        added = retain(features, solution, cases)
        print(f"Retain {added['id']}: case count {before} -> {len(cases)}")
        print("Stored problem:", json.dumps(added["problem"], sort_keys=True))
        print("Stored solution:", added["solution"])
        if args.case_file:
            args.case_file.write_text(json.dumps(cases, indent=2) + "\n",
                                      encoding="utf-8")
            print("Saved case base:", args.case_file.name)
        else:
            print("Learning retained in memory for this run.")


if __name__ == "__main__":
    main()
