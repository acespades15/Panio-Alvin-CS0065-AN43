# Asynchronous Activity 1 Student Early Warning Tool Using KNIME

This project uses academic performance indicators to classify a student as `At Risk` or `Not At Risk`. The workflow compares three supervised classification algorithms and evaluates each model with a Scorer node.

## Files

- `DemoEarlyWarningTool.knwf` - exported KNIME workflow with the dataset stored in its workflow data area
- `student_performance_knime.csv` - 30-record dataset used by the workflow
- `workflow.png` - screenshot of the completed KNIME workflow
- `Panio_Alvin_KNIME_GitHub_Evidence.pdf` - screenshots and records showing the completed workflow, repository files, Git commit, push, and public repository verification

## Features and target

The model uses `attendance`, `quiz_score`, `assignment_score`, and `exam_score` as input features. The `risk_status` column is the target. The `student_id` column is excluded from model training.

## Algorithms

- Logistic Regression
- Decision Tree
- Random Forest

## Workflow

`CSV Reader -> Column Filter -> Table Partitioner -> Learners -> Predictors -> Scorers`

## How to run

1. Download `DemoEarlyWarningTool.knwf` or clone this repository.
2. Open KNIME Analytics Platform and select **File > Import KNIME Workflow**.
3. Select `DemoEarlyWarningTool.knwf` and complete the import.
4. Open the CSV Reader configuration. It is configured for `student_performance_knime.csv` in the current workflow data area.
5. If KNIME asks for a source file, select the included `student_performance_knime.csv` from this folder and apply the configuration.
6. Execute all nodes.
7. Open the three Scorer nodes to review the confusion matrices and classification statistics.

## Responsible use

This is a small synthetic classroom dataset. The output is suitable for demonstrating a classification workflow, not for making real academic decisions. Any real use would require more representative data, validation, privacy safeguards, and human review.

## Author

Alvin Panio

## Course and section

CS0065 - AN43
