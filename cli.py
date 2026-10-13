import argparse, json
from main import ask

p = argparse.ArgumentParser(description="Offline merchant policy assistant")
p.add_argument("question", nargs="?", help="Question to ask")
p.add_argument("--date", default="2026-08-15", help="Policy date YYYY-MM-DD")
p.add_argument("--eval", action="store_true", help="Run eval.json")
args = p.parse_args()

if args.eval:
    cases = json.load(open("eval.json", encoding="utf-8"))
    rows = []
    for c in cases:
        got = ask(c["question"], c["as_of_date"])
        expected_status = c.get("expected_status")
        status_ok = (not expected_status or got["status"] == expected_status)
        
        expected_cits = c.get("expected_citations", [])
        got_cits = [str(cit).lower() for cit in got.get("citations", [])]
        
        if not expected_cits:
            citation_ok = True
        else:
            citation_ok = all(
                any(x.lower() in y for y in got_cits) for x in expected_cits
            )
            
        # DEBUG PRINTS FOR E11
        if c["id"] == "E11":
            print(f"\n--- DEBUG E11 ---")
            print(f"Expected in eval.json: {expected_cits}")
            print(f"Got from main.py:       {got.get('citations', [])}")
            print(f"Match result:           {citation_ok}")
            print(f"-------------------\n")

        rows.append((c, status_ok, citation_ok, got))
        
    print(f"{'ID':<5} {'STATUS':<8} {'CITATIONS':<10} QUESTION")
    for c, so, co, g in rows:
        print(f"{c['id']:<5} {('PASS' if so else 'FAIL'):<8} {('PASS' if co else 'FAIL'):<10} {c['question']}")
        
    print(f"Status score: {sum(x[1] for x in rows)}/{len(rows)}; citation score: {sum(x[2] for x in rows)}/{len(rows)}")

elif args.question:
    print(json.dumps(ask(args.question, args.date), ensure_ascii=False, indent=2))
else:
    p.print_help()