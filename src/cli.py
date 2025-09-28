"""Simple CLI for the banking app.

Supports running as a script (python src/cli.py) and as a module (python -m src.cli).
The module tries a package-relative import first and falls back to adding the src/ dir to sys.path.
"""

from __future__ import annotations

from pathlib import Path
import sys


try:
    # When executed as module: python -m src.cli
    from .bank.manager import AccountManager
except Exception:
    # Fallback when executed as script: python src/cli.py
    SRC_DIR = Path(__file__).resolve().parent
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
    from bank.manager import AccountManager


def _float_input(prompt: str, default: float = 0.0) -> float:
    s = input(prompt).strip()
    if s == "":
        return default
    try:
        return float(s)
    except ValueError:
        print("Invalid number, try again.")
        return _float_input(prompt, default)


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
                a = mgr.get(aid)
                if not a:
                    print("Account not found")
                else:
                    a.deposit(amt)
                    print(f"New balance: {a.balance}")
            elif cmd == "4":
                aid = input("Account id: ").strip()
                amt = _float_input("Amount: ")
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
                mgr.transfer(src, dst, amt)
                print("Transfer completed.")
            elif cmd == "6":
                for a in mgr.list_accounts():
                    owner = getattr(a, "owner", "")
                    print(f"{a.name}: {a.balance} {('- ' + owner) if owner else ''}")
            else:
                print("Unknown command")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()