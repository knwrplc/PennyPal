import argparse
from datetime import datetime
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


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    print(args)
    
if __name__ == "__main__":
    main() 