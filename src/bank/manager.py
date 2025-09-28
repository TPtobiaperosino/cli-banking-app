from __future__ import annotations

from typing import Dict, List, Optional
from bank.account import BankAccount


class AccountManager:
    """Manage BankAccount instances in-memory."""

    def __init__(self) -> None:
        self._accounts: Dict[str, BankAccount] = {}

    def create(self, account_id: str, owner: str = "", initial: float = 0.0) -> BankAccount:
        """Create and return a new BankAccount. Raises KeyError if id exists."""
        if account_id in self._accounts:
            raise KeyError(f"Account id '{account_id}' already exists.")
        acct = BankAccount(account_id, initial)
        # optional owner attribute for display
        if owner:
            setattr(acct, "owner", owner)
        self._accounts[account_id] = acct
        return acct

    def get(self, account_id: str) -> Optional[BankAccount]:
        return self._accounts.get(account_id)

    def list_accounts(self) -> List[BankAccount]:
        return list(self._accounts.values())

    def delete(self, account_id: str) -> None:
        self._accounts.pop(account_id, None)

    def transfer(self, src_id: str, dst_id: str, amount: float) -> None:
        src = self.get(src_id)
        dst = self.get(dst_id)
        if src is None or dst is None:
            raise KeyError("Source or destination account not found.")
        src.transfer(dst, amount)
