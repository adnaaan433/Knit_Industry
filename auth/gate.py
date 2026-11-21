"""Authentication gate enforcing login before any app UI or database query runs."""

import streamlit as st
from auth.login_page import render_login_page


def _get_stored_hash() -> str:
    try:
        val = st.secrets["app_password_hash"]
        return str(val).strip() if val else ""
    except Exception:
        return ""


def _render_setup_error():
    st.error("### Login Setup Required (`app_password_hash` missing)")
    st.markdown(
        """
        This application is configured to **fail closed** when `app_password_hash` is not set in Streamlit secrets.

        **To configure locally:**
        1. Run `python scripts/make_password_hash.py` in your terminal and enter your chosen password.
        2. Copy the output line (`app_password_hash = "pbkdf2$200000$..."`) into `.streamlit/secrets.toml`.

        **To configure on Streamlit Community Cloud:**
        1. Open your app's **Settings → Secrets** in Streamlit Community Cloud.
        2. Paste the `app_password_hash = "pbkdf2$200000$..."` line and save.
        """
    )


def require_login():
    """Block execution with st.stop() unless the visitor is authenticated."""
    if st.session_state.get("authenticated") is True:
        return

    stored_hash = _get_stored_hash()
    if not stored_hash or not stored_hash.startswith("pbkdf2$"):
        _render_setup_error()
        st.stop()

    render_login_page(stored_hash)
    st.stop()


def sign_out():
    """Clear authentication session state and return to the login page."""
    st.session_state.clear()
    st.query_params.clear()
    st.rerun()
