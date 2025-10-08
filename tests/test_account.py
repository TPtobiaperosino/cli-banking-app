import pytest

try:  # normal path when src/ is on PYTHONPATH
    from bank.account import BankAccount  # type: ignore
    from bank import exceptions as exc  # type: ignore
except Exception:  # pragma: no cover - secondary path if executed differently
    from src.bank.account import BankAccount  # type: ignore
    from src.bank import exceptions as exc  # type: ignore


@pytest.fixture()
def account() -> BankAccount:
    return BankAccount("Test Account", 1000)


def test_deposit(account: BankAccount):
    account.deposit(500)
    assert account.balance == 1500


def test_withdraw(account: BankAccount):
    account.withdraw(300)
    assert account.balance == 700


def test_withdraw_insufficient_funds(account: BankAccount):
    with pytest.raises(exc.InsufficientFundsError):
        account.withdraw(1200)


def test_transfer(account: BankAccount):
    target = BankAccount("Target Account", 500)
    account.transfer(target, 200)
    assert account.balance == 800
    assert target.balance == 700


def test_transfer_insufficient_funds(account: BankAccount):
    target = BankAccount("Target Account", 500)
    with pytest.raises(exc.InsufficientFundsError):
        account.transfer(target, 1200)