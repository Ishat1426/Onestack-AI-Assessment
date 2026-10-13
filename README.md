# The Policy That Changed — Offline Assistant

## Run

Requires Python 3.9+ and no third-party dependencies.

```bash
python cli.py "When does a small merchant receive UPI money?" --date 2026-08-15
python cli.py --eval
```

The `ask(question, as\_of\_date)` function returns `answer`, `citations`, and `status`.

## What works

* Deterministic, offline question answering for the assignment's policy topics.
* Effective-date handling for the 1 August 2026 circular and 1 September refund change.
* Fee arithmetic in code: MDR rate, cap, 18% GST, and total.
* Explicit citations to source documents and clauses.
* 14 locally runnable evaluation examples.

## Limitations

* This is a small rule-based prototype, not a general semantic search engine.
* Natural-language phrasing outside supported patterns may return `CANNOT\_ANSWER` or require additional rules.
* It does not model bank holidays, account-specific bank limits, or external policy updates.
* Validate all outputs against the source clauses before production use.



### **Evaluation**

* 
* Run the evaluation suite from the project root:
* 
* ```bash
* python cli.py --eval
* ```
* 
* The current evaluation contains 14 test cases. The latest local run passed all checks:
* 
* \- Status: 14/14
* \- Answer content: 14/14
* \- Citations: 14/14
* 
* These results apply to the included test cases and do not guarantee correctness for every possible policy question.

