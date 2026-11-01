# Technical Assessment 3

This folder contains a Case-Based Reasoning intelligent tutoring system created for CS0065 Intelligent Systems. The project demonstrates how stored experiences can be represented, retrieved, adapted, reviewed, and retained as new cases.

## Pair Members

- Alvin Christian S. Panio
- Faith Nemeño

The submission is recorded as equal pair work. Alvin and Faith share responsibility for understanding the program, checking its output, and reviewing the report and documentation before submission. Because the work was not divided into separate roles, this README does not claim different individual tasks for either partner.

## What the Pair Submission Includes

- A Python intelligent tutoring program that recommends practice for recurring math errors.
- A case representation containing the topic, error type, mastery score, repeated-error count, feedback, exercises, and outcome.
- A weighted similarity calculation for comparing a new problem with stored cases.
- A retrieval step that requires the same topic and error type before selecting the closest case.
- An adaptation step that changes the number of exercises and the amount of support.
- A revision step that requires a review note before a solution can be retained.
- A learning step that saves a successful reviewed case to a JSON case base and reloads it for future retrieval.
- A duplicate check that prevents an identical problem and solution from being stored repeatedly.
- A PDF report containing the explanation, complete program listing, reflection, validation results, and an actual Python IDLE execution screenshot.

## Files

- `TA3_Panio_Nemeño.pdf` — completed pair report.
- `tutoring_cbr.py` — runnable Case-Based Reasoning program.

## How the Program Works

1. **Represent** — store each tutoring experience as a structured case.
2. **Retrieve** — find a relevant past case using topic, error type, mastery, and repeated errors.
3. **Reuse and adapt** — reuse the feedback and adjust the exercises and support.
4. **Revise** — require a reviewer correction or confirmation.
5. **Retain** — save the reviewed successful experience as a new case.

## How to Run

Python 3.9 or later is recommended. The program uses only the Python standard library.

Run the repeatable demonstration:

```powershell
python tutoring_cbr.py --demo --case-base demo_cases.json
```

Run the interactive version:

```powershell
python tutoring_cbr.py --case-base cases.json
```

In a fresh demonstration, the program retrieves case `C01` with a similarity of `0.965`, adapts the recommendation to five exercises, retains new case `C06`, and retrieves `C06` with a similarity of `1.000` during the learning check. The seed cases and demonstrated outcome are illustrative educational data rather than actual student records.
