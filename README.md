# CLI Banking Application

## Overview
The CLI Banking Application is a simple command-line tool that allows users to manage their bank accounts. Users can create accounts, deposit and withdraw funds, transfer money between accounts, and check their balances. This project is designed to practice object-oriented programming and command-line interface development in Python.

## Features
Aurora Nexus Bank — CLI Banking App

Short summary
---------------
Aurora Nexus Bank — a minimal, well-tested CLI banking prototype with an optional Streamlit frontend. This project demonstrates clean OOP design, test coverage, a small UI layer, and domain-specific exception handling.

Why this is review-ready
------------------------
- Clear domain model: `BankAccount` encapsulates core operations (deposit, withdraw, transfer).
- Manager class: `AccountManager` provides a thin in-memory persistence layer and simple API.
- Domain exceptions: Distinct custom exceptions (`bank.exceptions`) enable precise error handling.
- Tests: pytest-based tests for accounts and manager with fixtures.
- Optional frontend: `streamlit_app.py` provides a polished demo UI.
- Tooling: Ruff (lint/format), mypy (typing), pytest + coverage configuration.

Quick start (macOS / Linux)
---------------------------
1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install pinned dependencies:

```bash
pip install -r requirements.txt
```

3. Run tests:

```bash
python -m pytest -q
```

4. Run the CLI:

```bash
python src/cli.py
```

5. Run the Streamlit frontend (optional demo):

```bash
streamlit run streamlit_app.py
```

If you are using an environment where the `streamlit` shim is not on `PATH`, run the module directly instead:

```bash
python -m streamlit run streamlit_app.py
```

Either command will start a local dev server (usually at `http://localhost:8501`) and open the app in your browser. Stop the server anytime with `Ctrl+C`. The Streamlit frontend provides an intuitive graphical interface for:
- Creating new bank accounts
- Making deposits and withdrawals
- Transferring money between accounts
- Viewing account balances and transaction history

Note: The Streamlit app uses in-memory storage, so data will be lost when you stop the server.

Project layout
--------------
- `src/` — application code
  - `bank/account.py` — domain model `BankAccount`
  - `bank/manager.py` — `AccountManager` in-memory storage
  - `bank/exceptions.py` — domain-specific exception types
  - `cli.py` — interactive terminal UI
- `streamlit_app.py` — optional Streamlit demo (in-memory state)
- `tests/` — unit tests and `conftest.py` that adds `src/` to PYTHONPATH for pytest
- `requirements.txt`, `pyproject.toml` — dependencies and project metadata

Quality & tooling
-----------------
Static analysis & formatting (installed via dev dependencies):
```bash
ruff check src tests   # lint
ruff format src tests  # format (or use --check in CI)
mypy src                # type checking
pytest -q --cov=src     # tests + coverage
```

Custom exception taxonomy (in `bank/exceptions.py`):
- `NegativeAmountError` – non-positive amount provided.
- `InsufficientFundsError` – withdrawal/transfer exceeds balance.
- `DuplicateAccountError` – account id already exists.
- `AccountNotFoundError` – source/destination not found.

