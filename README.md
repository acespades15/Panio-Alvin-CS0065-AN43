# CS0065 Intelligent Systems — Coursework Repository

This repository contains Alvin Christian S. Panio's coursework for **CS0065 — Intelligent Systems**, section **AN43-BSCSSE**. It includes four technical assessments with Python programs and PDF reports, plus a KNIME student early warning classification activity.

## Repository Contents

| Folder | Activity | Contents and concepts |
| --- | --- | --- |
| [TA1](TA1/) | Random Walk Simulation Using AgentPy | Agents move around a bounded grid while avoiding occupied cells. The program records paths, summarizes final positions, and creates a plot and animation. |
| [TA2](TA2/) | Rule-Based Vacuum Cleaner Agent | A two-room simulation that applies condition-action rules: clean a dirty room or move to the other room when the current room is clean. |
| [TA3](TA3/) | Case-Based Reasoning Intelligent Tutoring System | A math tutor retrieves similar cases, adapts practice and support, requires review, and saves successful experiences to a JSON case base. Pair work by Alvin Christian S. Panio and Faith Nemeño. |
| [TA4](TA4/) | Weather Knowledge and Reasoning | Illustrative weather facts demonstrate rule-based reasoning and the retrieve–reuse–revise–retain cycle of case-based reasoning, with optional JSON persistence. |
| [DemoEarlyWarningTool](DemoEarlyWarningTool/) | Asynchronous Activity 1: Student Early Warning Tool Using KNIME | A workflow compares Decision Tree, Logistic Regression, and Random Forest models to classify students as `At Risk` or `Not At Risk`. |

### TA1 — Random Walk Simulation

- [TA1_Panio.py](TA1/TA1_Panio.py) — interactive AgentPy simulation with configurable agent count, grid size, and number of steps.
- [TA1_Panio.pdf](TA1/TA1_Panio.pdf) — assessment report.

### TA2 — Rule-Based Vacuum Cleaner Agent

- [TA2_Panio.py](TA2/TA2_Panio.py) — interactive simulation that accepts each room's initial `Dirty` or `Clean` state and prints the agent's action and environment at each step.
- [TA2_Panio.pdf](TA2/TA2_Panio.pdf) — assessment report.

### TA3 — Case-Based Intelligent Tutoring

- [tutoring_cbr.py](TA3/tutoring_cbr.py) — tutoring program with weighted similarity, practice adaptation, review, duplicate prevention, and case retention.
- [TA3_Panio_Nemeño.pdf](TA3/TA3_Panio_Neme%C3%B1o.pdf) — pair assessment report.
- [README.md](TA3/README.md) — pair attribution, program explanation, and detailed run instructions.

### TA4 — Weather Reasoning

- [ta4_weather_reasoning.py](TA4/ta4_weather_reasoning.py) — weather reasoning demonstration using temperature, humidity, rain, outdoor activity, and umbrella availability. Supports rule-based and case-based modes, manual revision, and optional saved cases.
- [TA4_Panio.pdf](TA4/TA4_Panio.pdf) — assessment report.

### Asynchronous Activity 1 — KNIME Student Early Warning Tool

- [DemoEarlyWarningTool.knwf](DemoEarlyWarningTool/DemoEarlyWarningTool.knwf) — exported KNIME workflow, including the dataset in its workflow data area.
- [student_performance_knime.csv](DemoEarlyWarningTool/student_performance_knime.csv) — 30-record synthetic classroom dataset. Input features are attendance, quiz score, assignment score, and exam score; `risk_status` is the target and `student_id` is excluded from training.
- [workflow.png](DemoEarlyWarningTool/workflow.png) — screenshot of the completed workflow.
- [Panio_Alvin_KNIME_GitHub_Evidence.pdf](DemoEarlyWarningTool/Panio_Alvin_KNIME_GitHub_Evidence.pdf) — submission evidence.
- [README.md](DemoEarlyWarningTool/README.md) — dataset details, workflow steps, and import instructions.

### Repository Configuration

- [.gitignore](.gitignore) — excludes temporary and output directories from Git.
- [.gitattributes](.gitattributes) — marks KNIME workflow, PDF, and PNG files as binary.
- [README.md](README.md) — this repository overview.

## Running the Python Assessments

Use **Python 3.10 or later** as a common starting point for the assessments. TA2, TA3, and TA4 use only the Python standard library. TA1 additionally uses **AgentPy**, **Matplotlib**, and **Pillow** for animation export:

```powershell
python -m pip install agentpy matplotlib pillow
```

Run the following commands from the repository root. Run each assessment separately; TA1 and TA2 prompt for input.

### TA1

```powershell
python TA1/TA1_Panio.py
```

Enter the number of agents, grid size, and simulation steps. The number of agents cannot exceed the number of grid cells. The program saves `random_walk_paths.png` in the current working directory and displays an animation or exports `random_walk_animation.gif`, depending on the Matplotlib backend.

### TA2

```powershell
python TA2/TA2_Panio.py
```

Enter the initial state of rooms A and B and the number of simulation steps. The terminal shows the agent's location, action, and room states.

### TA3

Run the repeatable demonstration:

```powershell
python TA3/tutoring_cbr.py --demo --case-base TA3/demo_cases.json
```

Or run the interactive tutor:

```powershell
python TA3/tutoring_cbr.py --case-base TA3/cases.json
```

Successful reviewed cases are saved to the specified JSON file and can be loaded on later runs. These JSON files are generated by the program and are not included in the repository.

### TA4

Run both reasoning demonstrations:

```powershell
python TA4/ta4_weather_reasoning.py
```

Use `--mode rbr` or `--mode cbr` to select one reasoning method. To review the case-based recommendation interactively and save the case base:

```powershell
python TA4/ta4_weather_reasoning.py --mode cbr --interactive --case-file TA4/learned_cases.json
```

Without `--case-file`, learned cases remain in memory for the current run only. The JSON file is generated when saving is enabled.

## Running the KNIME Workflow

1. Open **KNIME Analytics Platform** and select **File > Import KNIME Workflow**.
2. Import [DemoEarlyWarningTool.knwf](DemoEarlyWarningTool/DemoEarlyWarningTool.knwf).
3. Open the CSV Reader configuration. The workflow includes the CSV in its data area; if KNIME asks for a file, select [student_performance_knime.csv](DemoEarlyWarningTool/student_performance_knime.csv).
4. Execute all nodes.
5. Open the three Scorer nodes to review the models' confusion matrices and classification statistics.

The workflow follows: **CSV Reader → Column Filter → Table Partitioner → Learners → Predictors → Scorers**.

## Educational Data

The KNIME dataset and the TA3 and TA4 example cases are illustrative educational data. TA4 does not retrieve live weather, and the KNIME activity demonstrates classification rather than providing a validated system for real academic decisions.

## Author and Course

- **Author:** Alvin Christian S. Panio
- **Course:** CS0065 — Intelligent Systems
- **Section:** AN43-BSCSSE
- **TA3 pair member:** Faith Nemeño
