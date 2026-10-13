import argparse
import json
from pathlib import Path

from main import ask

p = argparse.ArgumentParser(description="Offline merchant policy assistant")
p.add_argument("question", nargs="?", help="Question to ask")
p.add_argument("--date", default="2026-08-15", help="Policy date YYYY-MM-DD")
p.add_argument("--eval", action="store_true", help="Run eval.json")
args = p.parse_args()

if args.eval:
    eval_path = Path(__file__).with_name("eval.json")
    with eval_path.open(encoding="utf-8") as f:
        cases = json.load(f)

    rows = []

    for case in cases:
        got = ask(case["question"], case["as_of_date"])

        expected_status = case.get("expected_status")
        status_ok = (
            not expected_status
            or got.get("status") == expected_status
        )

        # Check that all expected key phrases appear in the generated answer.
        expected_phrases = case.get("expected_answer_contains", [])
        answer_text = str(got.get("answer", "")).casefold()
        answer_ok = all(
            str(phrase).casefold() in answer_text
            for phrase in expected_phrases
        )

        expected_citations = case.get("expected_citations", [])
        got_citations = [
            str(citation).casefold()
            for citation in got.get("citations", [])
        ]
        citation_ok = all(
            any(str(expected).casefold() in actual for actual in got_citations)
            for expected in expected_citations
        )

        rows.append((case, status_ok, answer_ok, citation_ok, got))

    print(f"{'ID':<5} {'STATUS':<8} {'ANSWER':<8} {'CITATIONS':<10} QUESTION")
    for case, status_ok, answer_ok, citation_ok, _got in rows:
        print(
            f"{case['id']:<5} "
            f"{'PASS' if status_ok else 'FAIL':<8} "
            f"{'PASS' if answer_ok else 'FAIL':<8} "
            f"{'PASS' if citation_ok else 'FAIL':<10} "
            f"{case['question']}"
        )

    total = len(rows)
    status_score = sum(row[1] for row in rows)
    answer_score = sum(row[2] for row in rows)
    citation_score = sum(row[3] for row in rows)

    print(
        f"Status score: {status_score}/{total}; "
        f"answer score: {answer_score}/{total}; "
        f"citation score: {citation_score}/{total}"
    )

    failed_answers = [
        (case["id"], case["question"], got.get("answer", ""))
        for case, _status_ok, answer_ok, _citation_ok, got in rows
        if not answer_ok
    ]
    if failed_answers:
        print("\nAnswer-content failures (inspect these; do not just weaken the tests):")
        for case_id, question, answer in failed_answers:
            print(f"\n{case_id}: {question}\nActual answer: {answer}")

elif args.question:
    print(
        json.dumps(
            ask(args.question, args.date),
            ensure_ascii=False,
            indent=2,
        )
    )
else:
    p.print_help()
