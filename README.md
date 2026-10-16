# Asynchronous Activity 1: Student Early Warning Tool Using KNIME

This repository contains Alvin Christian S. Panio's KNIME submission for Asynchronous Activity 1. The workflow uses academic performance data to classify students as `At Risk` or `Not At Risk`.

## Files

- [DemoEarlyWarningTool.knwf](DemoEarlyWarningTool/DemoEarlyWarningTool.knwf) — exported KNIME workflow, including a copy of the dataset in its workflow data area.
- [student_performance_knime.csv](DemoEarlyWarningTool/student_performance_knime.csv) — 30-record dataset used by the workflow.
- [workflow.png](DemoEarlyWarningTool/workflow.png) — screenshot of the completed workflow.
- [Panio_Alvin_KNIME_GitHub_Evidence.pdf](DemoEarlyWarningTool/Panio_Alvin_KNIME_GitHub_Evidence.pdf) — submission evidence.
- [DemoEarlyWarningTool/README.md](DemoEarlyWarningTool/README.md) — more details about the dataset and workflow.

The repository also contains separate coursework files in [TA1](TA1/) and [TA2](TA2/).

## Algorithms

- Decision Tree
- Logistic Regression
- Random Forest

## How to Run

1. Download the workflow and CSV file above, or clone this repository.
2. In KNIME Analytics Platform, select **File > Import KNIME Workflow** and import `DemoEarlyWarningTool.knwf`.
3. Open the CSV Reader configuration. The workflow includes the CSV in its data area; if KNIME asks for a file, select `student_performance_knime.csv` from the `DemoEarlyWarningTool` folder.
4. Execute all nodes.
5. Open the three Scorer nodes to review the evaluation results.

## Author

Alvin Christian S. Panio

## Course and Section

CS0065 - AN43-BSCSSE
