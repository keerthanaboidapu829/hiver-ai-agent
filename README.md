# AppleSupport AI Support Agent — Hiver SDE Intern Take-Home

A proof-first customer-support agent built on the Customer Support on Twitter (TWCS) dataset, using **AppleSupport** as the selected brand.

## What the system does

`customer message → intent classification → historical retrieval → grounded reply draft → auto-handle / escalate`

The design deliberately keeps historical support replies as evidence instead of inventing unsupported policy or product facts.

### Intent taxonomy

- `software_update` — iOS/macOS updates and update-related issues
- `device_hardware` — physical device, screen, buttons and hardware issues
- `battery_charging` — battery drain, battery health, charging and chargers
- `app_service` — Apple apps/services such as Music, App Store, iCloud and Files
- `connectivity` — Wi-Fi, Bluetooth, cellular, calls and network connectivity
- `account_purchase` — Apple ID, passwords, subscriptions, payments, purchases and refunds
- `general_support` — genuine support questions that do not fit the above

## Repository structure

```text
.
├── data/
│   └── README.md
├── evaluation/
│   ├── golden_set.csv
│   ├── evaluate.py
│   └── judge_rubric.md
├── report/
│   └── report.md
├── src/
│   ├── data_processing.py
│   ├── escalation.py
│   ├── intent_classifier.py
│   ├── pipeline.py
│   ├── reply_generator.py
│   └── retrieval.py
├── decision_log.md
├── requirements.txt
└── README.md
```

## Quick start

Create an environment and install dependencies:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Download the TWCS Kaggle CSV and place it at `data/twcs.csv`. The raw dataset is intentionally not committed to GitHub.

Then run:

```bash
python src/data_processing.py
python src/intent_classifier.py
python evaluation/evaluate.py
```

The processing script extracts customer → AppleSupport response pairs. The classifier trains a TF-IDF + Logistic Regression intent model from the golden/evaluation labels.

## Evaluation discipline

The assignment requires a **150–250 example hand-labelled golden set**. The checked-in `evaluation/golden_set.csv` is only a starter set and must be expanded and manually reviewed before final headline metrics are reported. Suggested/keyword-generated labels are not treated as human ground truth.

The evaluation plan includes:

1. Majority-class trivial baseline.
2. TF-IDF + Logistic Regression simple baseline.
3. Intent metrics including accuracy and macro-F1.
4. Retrieval evidence quality.
5. LLM-as-judge reply scoring for relevance, groundedness, helpfulness, tone and non-hallucination.
6. Human-vs-LLM judge agreement on a held-out human-reviewed subset.
7. Explicit escalation reasoning for low-confidence or weak-evidence cases.

## Important limitations

This repository is intentionally transparent about what is and is not implemented. Full multi-turn thread reconstruction, a production LLM response generator, a 150–250 example human-labelled golden set, calibrated judge agreement and final benchmark numbers still require completion/verification on the full supplied dataset. No fabricated benchmark is included.

See `report/report.md` and `decision_log.md` for the framing, failure modes, evaluation plan and non-obvious decisions.

## Data provenance

Dataset: Customer Support on Twitter (TWCS), downloaded from Kaggle. See `data/README.md` for expected columns and setup instructions. Any borrowed code/material should be cited before submission.
