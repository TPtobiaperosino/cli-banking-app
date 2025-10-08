"""Simple CLI for the banking app.

Execution modes:
    python -m src.cli
    python src/cli.py

If the package is installed (``pip install -e .``) the relative import path is
used. Otherwise we fall back to injecting the local ``src`` path for an ad‑hoc
run. For a cleaner environment prefer installing in editable mode.
"""

from __future__ import annotations

from pathlib import Path
import sys


try:  # First attempt: package-relative import (installed or run as module)
    from .bank.manager import AccountManager  # type: ignore
    from .bank import exceptions as exc  # type: ignore
except Exception:  # pragma: no cover - fallback path
    SRC_DIR = Path(__file__).resolve().parent
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
    from bank.manager import AccountManager  # type: ignore
    from bank import exceptions as exc  # type: ignore


def _float_input(prompt: str, default: float | None = None) -> float:
    """Prompt user for a positive float (or any float if default provided)."""
    while True:
        s = input(prompt).strip()
        if s == "" and default is not None:
            return default
        try:
            value = float(s)
            return value
        except ValueError:
            print("Invalid number, try again.")


def main() -> None:
    mgr = AccountManager()
    while True:
        print("\n1) Create  2) Balance  3) Deposit  4) Withdraw  5) Transfer  6) List  0) Quit")
        cmd = input("Choose: ").strip()
        try:
            if cmd == "0":
                break
            if cmd == "1":
                aid = input("Account id: ").strip()
                owner = input("Owner (optional): ").strip()
                initial = _float_input("Initial (default 0): ", 0.0)
                if initial < 0:
                    print("Initial balance cannot be negative.")
                    continue
                acct = mgr.create(aid, owner, initial)
                print(f"Created {acct.name} with balance {acct.balance}")
            elif cmd == "2":
                aid = input("Account id: ").strip()
                a = mgr.get(aid)
                if a:
                    print(f"Balance: {a.balance}")
                else:
                    print("Account not found")
            elif cmd == "3":
                aid = input("Account id: ").strip()
                amt = _float_input("Amount: ")
                if amt <= 0:
                    print("Amount must be positive.")
                    continue
                a = mgr.get(aid)
                if not a:
                    print("Account not found")
                else:
                    a.deposit(amt)
                    print(f"New balance: {a.balance}")
            elif cmd == "4":
                aid = input("Account id: ").strip()
                amt = _float_input("Amount: ")
                if amt <= 0:
                    print("Amount must be positive.")
                    continue
                a = mgr.get(aid)
                if not a:
                    print("Account not found")
                else:
                    a.withdraw(amt)
                    print(f"New balance: {a.balance}")
            elif cmd == "5":
                src = input("From id: ").strip()
                dst = input("To id: ").strip()
                amt = _float_input("Amount: ")
                if amt <= 0:
                    print("Amount must be positive.")
                    continue
                mgr.transfer(src, dst, amt)
                print("Transfer completed.")
            elif cmd == "6":
                for a in mgr.list_accounts():
                    owner = getattr(a, "owner", "")
                    print(f"{a.name}: {a.balance} {('- ' + owner) if owner else ''}")
            else:
                print("Unknown command")
        except Exception as e:  # broad catch to keep CLI interactive
            # Provide friendlier labels for known domain errors.
            prefix = "Error"
            if hasattr(e, "__class__") and e.__class__.__name__.endswith("Error"):
                prefix = e.__class__.__name__
            print(f"{prefix}: {e}")


if __name__ == "__main__":
    main()