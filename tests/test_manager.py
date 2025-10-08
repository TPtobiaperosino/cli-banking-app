import pytest

try:
    from bank.manager import AccountManager  # type: ignore
    from bank import exceptions as exc  # type: ignore
except Exception:  # pragma: no cover
    from src.bank.manager import AccountManager  # type: ignore
    from src.bank import exceptions as exc  # type: ignore

def test_create_and_get():
    mgr = AccountManager()
    a = mgr.create("A1", "Alice", 100.0)
    assert mgr.get("A1") is a
    assert a.balance == 100.0


def test_duplicate_create_raises():
    mgr = AccountManager()
    mgr.create("A1", "Alice", 0.0)
    with pytest.raises(exc.DuplicateAccountError):
        mgr.create("A1", "Bob", 0.0)


def test_transfer_success():
    mgr = AccountManager()
    mgr.create("A1", "Alice", 1000.0)
    mgr.create("A2", "Bob", 500.0)
    mgr.transfer("A1", "A2", 200.0)
    assert pytest.approx(mgr.get("A1").balance) == 800.0
    assert pytest.approx(mgr.get("A2").balance) == 700.0


def test_transfer_missing_account_raises():
    mgr = AccountManager()
    mgr.create("A1", "Alice", 100.0)
    with pytest.raises(exc.AccountNotFoundError):
        mgr.transfer("A1", "X", 50.0)


def test_delete_and_list():
    mgr = AccountManager()
    mgr.create("A1", "Alice", 10.0)
    mgr.create("A2", "Bob", 20.0)
    names = {a.name for a in mgr.list_accounts()}
    assert names == {"A1", "A2"}
    mgr.delete("A1")
    assert mgr.get("A1") is None

