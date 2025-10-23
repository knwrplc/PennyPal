import argparse
from datetime import date
from typing import Any, Dict, List
from storage import load_ledger, save_ledger
        
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog = "PennyPal",
        description = "CLI expense tracker"
    )
    sub = p.add_subparsers(
        dest = "cmd",
        required = True
    )
    
    add = sub.add_parser("add", help="Add a new expense")
    add.add_argument("--date")
    add.add_argument("--amount", type=float, required=True)
    add.add_argument("--category", required=True)
    add.add_argument("--note", default="")
    
    sub.add_parser("list", help = "List all expenses")
    
    return p

def cmd_add(args) -> None:
    d = args.date or date.today().isoformat()
    kind = "income" if args.amount >= 0 else "expense"
    row = {
        "date" : d,
        "amount" : float(args.amount),
        "category" : args.category,
        "note" : args.note,
        "kind" : kind
        }

    ledger = load_ledger()
    ledger.append(row)
    save_ledger(ledger)
    
    print(f"Added: {d} | {args.amount:>8.2f} | {args.category} | {args.note}")

def cmd_list(args) -> None:
    ledger = load_ledger()
    if not ledger:
        print("No expenses yet.")
        return
    
    print("DATE        AMOUNT   KIND      CATEGORY    NOTE")
    print("-" * 60)
    for r in ledger:
        print(f"{r['date']}  {r['amount']:>8.2f}  {r['kind']:<8}  {r['category']:<10}  {r['note']}")

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    
    if args.cmd == "add":
        cmd_add(args)
    elif args.cmd == "list":
        cmd_list(args)
    
if __name__ == "__main__":
    main() 