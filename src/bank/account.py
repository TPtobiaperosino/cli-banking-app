from __future__ import annotations
from typing import Union
from bank.exceptions import (
    NegativeAmountError,
    InsufficientFundsError,
)

Number = Union[int, float]


class BankAccount:
    """Simple in‑memory bank account.

    NOTE: Uses ``float`` for simplicity. For real financial applications use
    :class:`decimal.Decimal` with an agreed context to avoid floating point
    rounding issues.
    """

    def __init__(self, name: str, balance: Number = 0.0) -> None:
        self.name = str(name)
        self.balance = float(balance)

    def deposit(self, amount: Number) -> float:
        if not isinstance(amount, (int, float)):
            raise TypeError("Deposit amount must be a number.")
        if amount <= 0:
            raise NegativeAmountError("Deposit amount must be positive.")
        self.balance += float(amount)
        return self.balance

    def withdraw(self, amount: Number) -> float:
        if not isinstance(amount, (int, float)):
            raise TypeError("Withdrawal amount must be a number.")
        if amount <= 0:
            raise NegativeAmountError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds.")
        self.balance -= float(amount)
        return self.balance

    def transfer(self, target_account: "BankAccount", amount: Number) -> None:
        """Transfer ``amount`` from this account to ``target_account``.

        Operation is simple: withdraw then deposit. If withdrawal fails (e.g.
        insufficient funds) the deposit is never attempted.
        """
        if not isinstance(target_account, BankAccount):
            raise TypeError("target_account must be a BankAccount instance.")
        if not isinstance(amount, (int, float)):
            raise TypeError("Transfer amount must be a number.")
        if amount <= 0:
            raise NegativeAmountError("Transfer amount must be positive.")
        # reuse withdraw/deposit to keep validation consistent
        self.withdraw(amount)
        target_account.deposit(amount)