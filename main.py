import argparse
from datetime import date
from typing import Any, Dict, List
from storage import load_ledger, save_ledger
import sys

def parse_date_or_today(raw: str | None ) -> str:
    if raw is None or raw == "":
        return date.today().isoformat()
    try:
        parsed = date.fromisoformat(raw)
    except ValueError: 
        raise InvalidInputError("Date must be in YYYY-MM-DD format")
    return parsed.isoformat()

class InvalidInputError(Exception):
    pass
        
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
    try:
        d = parse_date_or_today(args.date)
    except InvalidInputError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
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
        print("No transactions yet.")
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