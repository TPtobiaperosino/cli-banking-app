from pathlib import Path
import sys
from typing import List, Dict

# ensure src is importable when running Streamlit from project root
PROJECT_ROOT = Path(__file__).resolve().parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

try:
    from bank.manager import AccountManager  # type: ignore
except Exception:  # pragma: no cover - fallback for direct execution without editable install
    # attempt to append src again in edge cases
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    from bank.manager import AccountManager  # type: ignore


def fmt(amount: float) -> str:
    return f"{amount:,.2f}"


def run_app():
    # Import Streamlit only when running the app to avoid import-time side effects
    import streamlit as st

    def ensure_session_state():
        if "mgr" not in st.session_state:
            st.session_state.mgr = AccountManager()
        if "tx_history" not in st.session_state:
            st.session_state.tx_history = []

    ensure_session_state()
    mgr: AccountManager = st.session_state.mgr

    # Page config and branding
    st.set_page_config(page_title="Aurora Nexus Bank — Online Banking", layout="wide")

    # Inject custom CSS to give a conservative, professional banking look (deep navy + gold accent)
    css = """
    <style>
    :root{--navy:#071a3a; --bank-dark:#071a3a; --gold:#c9a84a; --muted:#6b7280; --card:#ffffff}
    /* Page background */
    .css-1d391kg { background-color: #f4f6f9; }
    /* Top navigation */
    .top-nav { display:flex; align-items:center; justify-content:space-between; padding:18px 14px; background:linear-gradient(90deg,#07203a,#0b2b4a); color: white; border-radius:6px; margin-bottom:18px }
    .brand { font-size:28px; font-weight:700; letter-spacing:0.4px }
    .brand-sub { font-size:12px; color: rgba(255,255,255,0.85); margin-left:8px }
    .nav-actions button { background: transparent; border:1px solid rgba(255,255,255,0.12); color: white; padding:8px 12px; border-radius:6px }
    /* Headings */
    .stMarkdown h1, .stMarkdown h2 { color: var(--navy); }
    /* Subheaders */
    .stSubheader { color: var(--navy); font-weight:600; }
    /* Buttons */
    div.stButton>button, button[kind] { background-color: var(--navy) !important; color: white !important; border-radius: 6px !important; }
    /* Sidebar / action panel look */
    .css-1lcbmhc { background: var(--card); border: 1px solid #e8eef6; border-radius:8px; padding:12px }
    /* Table header */
    .stTable th { background: linear-gradient(90deg, #f7f9fc, #eef4ff); color: var(--navy); }
    /* Transaction history style */
    .stExpander > button { color: var(--navy); }
    /* Muted caption */
    footer, .css-1ypv5cq { color: var(--muted); }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Top navigation / brand bar
    nav_html = """
    <div class='top-nav'>
        <div class='brand'>Aurora Nexus Bank <span class='brand-sub'>— Private & Business Banking</span></div>
        <div class='nav-actions'>
            <button onclick="window.location.href='#'">Login</button>
        </div>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)

    with st.container():
        left, right = st.columns([3, 1])

        with left:
            st.subheader("Accounts")
            accounts = mgr.list_accounts()
            if accounts:
                # build a simple table with formatted balances
                rows = [{"id": a.name, "balance": fmt(a.balance), "owner": getattr(a, "owner", "")} for a in accounts]
                st.table(rows)
            else:
                st.info("No accounts yet. Use the Actions panel to create one.")

            # transaction history expander
            with st.expander("Transaction history"):
                if st.session_state.tx_history:
                    for tx in reversed(st.session_state.tx_history[-50:]):
                        st.write(f"- [{tx['time']}] {tx['message']}")
                else:
                    st.write("No transactions yet.")

        with right:
            st.subheader("Actions")

            # Use forms to group inputs and avoid immediate reruns
            action = st.selectbox("Choose action", ["Create", "Deposit", "Withdraw", "Transfer", "Delete"])

            if action == "Create":
                with st.form("create_form"):
                    aid = st.text_input("Account id")
                    owner = st.text_input("Owner (optional)")
                    initial = st.number_input("Initial balance", value=0.0, step=1.0)
                    submitted = st.form_submit_button("Create account")
                if submitted:
                    if not aid:
                        st.error("Account id is required")
                    else:
                        try:
                            mgr.create(aid.strip(), owner.strip(), float(initial))
                            st.success(f"Created account {aid}")
                            st.session_state.tx_history.append({"time": __import__("datetime").datetime.now().isoformat(timespec='seconds'), "message": f"Created {aid} (owner={owner}) initial={fmt(initial)}"})
                        except Exception as e:
                            st.error(str(e))

            elif action in ("Deposit", "Withdraw"):
                ids = [a.name for a in mgr.list_accounts()]
                if not ids:
                    st.warning("No accounts available")
                else:
                    with st.form(f"{action.lower()}_form"):
                        aid = st.selectbox("Account", ids)
                        amt = st.number_input("Amount", value=0.0, step=1.0)
                        submitted = st.form_submit_button(action)
                    if submitted:
                        a = mgr.get(aid)
                        try:
                            if action == "Deposit":
                                a.deposit(float(amt))
                                st.success(f"Deposited {fmt(amt)} to {aid}")
                                st.session_state.tx_history.append({"time": __import__("datetime").datetime.now().isoformat(timespec='seconds'), "message": f"Deposit {fmt(amt)} to {aid}"})
                            else:
                                a.withdraw(float(amt))
                                st.success(f"Withdrew {fmt(amt)} from {aid}")
                                st.session_state.tx_history.append({"time": __import__("datetime").datetime.now().isoformat(timespec='seconds'), "message": f"Withdraw {fmt(amt)} from {aid}"})
                        except Exception as e:
                            st.error(str(e))

            elif action == "Transfer":
                ids = [a.name for a in mgr.list_accounts()]
                if len(ids) < 2:
                    st.warning("Need at least two accounts")
                else:
                    with st.form("transfer_form"):
                        src = st.selectbox("From", ids, index=0)
                        dst = st.selectbox("To", ids, index=1)
                        amt = st.number_input("Amount", value=0.0, step=1.0)
                        submitted = st.form_submit_button("Transfer")
                    if submitted:
                        try:
                            mgr.transfer(src, dst, float(amt))
                            st.success(f"Transferred {fmt(amt)} from {src} to {dst}")
                            st.session_state.tx_history.append({"time": __import__("datetime").datetime.now().isoformat(timespec='seconds'), "message": f"Transfer {fmt(amt)} {src} -> {dst}"})
                        except Exception as e:
                            st.error(str(e))

            elif action == "Delete":
                ids = [a.name for a in mgr.list_accounts()]
                if not ids:
                    st.warning("No accounts available")
                else:
                    with st.form("delete_form"):
                        aid = st.selectbox("Account to delete", ids)
                        submitted = st.form_submit_button("Delete")
                    if submitted:
                        mgr.delete(aid)
                        st.success(f"Deleted {aid}")
                        st.session_state.tx_history.append({"time": __import__("datetime").datetime.now().isoformat(timespec='seconds'), "message": f"Deleted {aid}"})

    st.markdown("---")
    st.caption("Data in memory only — restart app to reset.")


if __name__ == "__main__":
    run_app()
