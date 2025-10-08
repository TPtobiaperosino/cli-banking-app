"""Domain-specific exception types for the banking application.

Having explicit exception classes makes error handling clearer and allows
callers (CLI / API / UI) to selectively catch only what they expect.
"""
from __future__ import annotations


class BankingError(Exception):
    """Base class for all banking related exceptions."""


class NegativeAmountError(BankingError):
    """Raised when an operation receives a non-positive monetary amount."""


class InsufficientFundsError(BankingError):
    """Raised when a withdrawal or transfer would overdraw an account."""


class DuplicateAccountError(BankingError):
    """Raised when attempting to create an account whose id already exists."""


class AccountNotFoundError(BankingError):
    """Raised when referencing an account id that does not exist."""