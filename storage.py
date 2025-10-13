from pathlib import Path
from typing import Any, Dict, List
import json

DATA_PATH = Path("data/ledger.json")

def load_ledger() -> List[Dict[str, Any]]:
    _ensure_file()
    text = DATA_PATH.read_text(encoding="utf-8")
    try:
        rows = json.loads(text)
    except json.JSONDecodeError:
        rows = []
    return rows

def save_ledger(rows: List[Dict[str, Any]]) -> None:
    _ensure_file()
    text = json.dumps(rows, ensure_ascii= False, indent=2)
    DATA_PATH.write_text(text, encoding="utf-8")

def _ensure_file() -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_PATH.exists():
        DATA_PATH.write_text("[]", encoding="utf-8")