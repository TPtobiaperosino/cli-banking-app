from __future__ import annotations

from typing import Dict, List, Optional
from bank.account import BankAccount
from bank.exceptions import (
    DuplicateAccountError,
    AccountNotFoundError,
)


class AccountManager:
    """Manage BankAccount instances in-memory."""

    def __init__(self) -> None:
        self._accounts: Dict[str, BankAccount] = {}

    def create(self, account_id: str, owner: str = "", initial: float = 0.0) -> BankAccount:
        """Create and return a new :class:`BankAccount`.

        Raises:
            KeyError: if ``account_id`` already exists.
        """
        if account_id in self._accounts:
            raise DuplicateAccountError(f"Account id '{account_id}' already exists.")
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
        if src is None:
            raise AccountNotFoundError(f"Source account '{src_id}' not found.")
        if dst is None:
            raise AccountNotFoundError(f"Destination account '{dst_id}' not found.")
        src.transfer(dst, amount)
