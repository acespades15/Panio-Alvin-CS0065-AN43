"""TA3: a small case-based math tutor. All seed and demo data are illustrative."""
import argparse
import copy
import json
from pathlib import Path


def make_case(cid, topic, error, mastery, repeats, feedback, exercises):
    return {"id": cid, "problem": {"topic": topic, "error": error,
            "mastery": mastery, "repeats": repeats},
            "solution": {"feedback": feedback, "exercises": exercises},
            "outcome": "Successful intervention in illustrative seed data."}


SEEDS = [
    make_case("C01", "linear equations", "sign", 30, 3,
              "Apply the same inverse operation to both sides; track each sign.", 4),
    make_case("C02", "linear equations", "distribution", 45, 2,
              "Multiply every term inside brackets, including its sign.", 3),
    make_case("C03", "linear equations", "balance", 60, 2,
              "Write each operation on both sides before simplifying.", 3),
    make_case("C04", "fractions", "denominator", 35, 4,
              "Find a common denominator before adding numerators.", 4),
    make_case("C05", "area", "formula", 50, 2,
              "Identify the shape and label dimensions before choosing a formula.", 3),
]


def validate(problem):
    """Reject malformed feature values before distance calculations."""
    for key in ("topic", "error"):
        if not isinstance(problem.get(key), str) or not problem[key].strip():
            raise ValueError(f"{key} must be nonempty text")
    for key, low, high in (("mastery", 0, 100), ("repeats", 1, 5)):
        value = problem.get(key)
        if type(value) is not int or not low <= value <= high:
            raise ValueError(f"{key} must be an integer from {low} to {high}")


def similarity(new, old):
    """Weighted score in [0, 1]; numeric distances use fixed domain ranges."""
    validate(new)
    validate(old)
    return (0.25 * (new["topic"] == old["topic"])
            + 0.45 * (new["error"] == old["error"])
            + 0.20 * (1 - abs(new["mastery"] - old["mastery"]) / 100)
            + 0.10 * (1 - abs(new["repeats"] - old["repeats"]) / 4))


def retrieve(problem, cases):
    """Only reuse cases with the same topic AND error; break ties by ID."""
    validate(problem)
    candidates = [(similarity(problem, c["problem"]), c) for c in cases
                  if all(problem[k] == c["problem"][k]
                         for k in ("topic", "error"))]
    if not candidates:
        raise ValueError("No matching topic/error case; ask a teacher for a new case.")
    return sorted(candidates, key=lambda item: (-item[0], item[1]["id"]))[0]


def adapt(problem, case):
    """Reuse past feedback, then adjust practice and scaffolding."""
    solution = copy.deepcopy(case["solution"])
    delta = problem["repeats"] - case["problem"]["repeats"]
    solution["exercises"] = max(2, min(8, solution["exercises"] + delta))
    solution["support"] = ("Show one fully worked example, then fade hints."
                           if problem["mastery"] < 40 else
                           "Start with a hint, then solve independently.")
    return solution


def revise(solution, review_note):
    """A reviewer supplies an explicit correction or confirmation."""
    if not review_note.strip():
        raise ValueError("A review note is required before retention")
    revised = copy.deepcopy(solution)
    revised["review"] = review_note.strip()
    return revised


def retain(cases, problem, solution, outcome, source_id):
    """Retain only reviewed solutions with a recorded successful outcome."""
    validate(problem)
    if not solution.get("review") or not outcome.strip():
        raise ValueError("Reviewed solution and successful outcome are required")
    for case in cases:
        if case["problem"] == problem and case["solution"] == solution:
            return case, False  # Re-running the same demonstration is idempotent.
    next_id = max((int(c["id"][1:]) for c in cases), default=0) + 1
    case = {"id": f"C{next_id:02d}", "problem": copy.deepcopy(problem),
            "solution": copy.deepcopy(solution), "outcome": outcome.strip(),
            "retrieved_from": source_id}
    cases.append(case)
    return case, True


def load_cases(path):
    if not path.exists():
        return copy.deepcopy(SEEDS)
    cases = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        raise ValueError("Case base must contain a JSON list")
    ids = set()
    for case in cases:
        validate(case["problem"])
        cid = case["id"]
        if not (isinstance(cid, str) and cid.startswith("C")
                and cid[1:].isdigit()) or cid in ids:
            raise ValueError("Case IDs must be unique C-prefixed integers")
        ids.add(cid)
        solution = case["solution"]
        if (not isinstance(solution.get("feedback"), str)
                or not solution["feedback"].strip()
                or type(solution.get("exercises")) is not int
                or not 2 <= solution["exercises"] <= 8):
            raise ValueError("Invalid stored solution")
    return cases


def save_cases(path, cases):
    """Replace atomically after a complete JSON write."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def run(path, demo=False):
    cases = load_cases(path)
    print("INTELLIGENT TUTORING SYSTEM - CASE-BASED REASONING")
    print("Seed/demo records are illustrative, not actual student records.")
    print(f"Case base before: {len(cases)} cases")
    if demo:
        problem = {"topic": "linear equations", "error": "sign",
                   "mastery": 35, "repeats": 4}
    else:
        print("Available topic/error pairs: " + "; ".join(sorted({
            f'{c["problem"]["topic"]}/{c["problem"]["error"]}' for c in cases})))
        problem = {"topic": input("Topic: ").strip().lower(),
                   "error": input("Error: ").strip().lower(),
                   "mastery": int(input("Mastery (0-100): ")),
                   "repeats": int(input("Repeated errors (1-5): "))}
    print("INPUT:", json.dumps(problem, sort_keys=True))
    score, matched = retrieve(problem, cases)
    print(f'RETRIEVE: {matched["id"]}, similarity = {score:.3f}')
    print("REUSE:", matched["solution"]["feedback"])
    solution = adapt(problem, matched)
    print(f'ADAPT: {solution["exercises"]} practice exercises')
    print("SUPPORT:", solution["support"])
    review = ("Check the answer by substituting into the original equation."
              if demo else input("Reviewer correction/confirmation: "))
    solution = revise(solution, review)
    print("REVISE:", solution["review"])
    if demo:
        success = True
        outcome = "Illustrative practice check: 3 of 4 answers correct."
    else:
        success = input("Was the intervention successful? (yes/no): ").lower() == "yes"
        outcome = input("Describe observed outcome: ") if success else ""
    if not success:
        print("RETAIN: deferred; revise the intervention with a teacher.")
        return
    learned, added = retain(cases, problem, solution, outcome, matched["id"])
    save_cases(path, cases)
    print(f'RETAIN: {learned["id"]} ' + ("added" if added else "already stored"))
    print("OUTCOME:", learned["outcome"])
    print(f"Case base after reload: {len(load_cases(path))} cases")
    print("UPDATED CASE LIST (ID | topic | error | mastery | repeats | exercises):")
    for case in load_cases(path):
        p, s = case["problem"], case["solution"]
        print(f'{case["id"]} | {p["topic"]} | {p["error"]} | '
              f'{p["mastery"]} | {p["repeats"]} | {s["exercises"]}')
    new_score, new_match = retrieve(problem, load_cases(path))
    print(f'LEARNING CHECK: {new_match["id"]}, similarity = {new_score:.3f}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-base", type=Path, default=Path("cases.json"))
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    try:
        run(args.case_base, args.demo)
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, f"Input/case-base error: {error}\n")
