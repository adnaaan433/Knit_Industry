"""Renders the on-theme password login page with brute-force lockout protection."""

from datetime import datetime, timedelta, timezone
import html
import os
import random
import time
import streamlit as st
from auth.facts import TEXTILE_FACTS
from auth.security import verify_password

MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 60
DHAKA_TZ = timezone(timedelta(hours=6))


def _dhaka_greeting() -> str:
    hour = datetime.now(DHAKA_TZ).hour
    if 5 <= hour < 12:
        return "Good morning"
    if 12 <= hour < 17:
        return "Good afternoon"
    return "Good evening"


def _load_login_css():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    css_path = os.path.join(root, "theme", "login.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f_css:
            st.markdown(f"<style>{f_css.read()}</style>", unsafe_allow_html=True)


def _brand_svg_html() -> str:
    return (
        '<div class="yarn-orb-wrap"><div class="yarn-orb yarn-orb-1"></div><div class="yarn-orb yarn-orb-2"></div></div>'
        '<div class="login-brand-block">'
        '<svg class="needle-mark-svg" viewBox="0 0 54 54" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<line x1="10" y1="44" x2="42" y2="12" stroke="#2563eb" stroke-width="2.6" stroke-linecap="round"/>'
        '<circle cx="43.5" cy="10.5" r="3" fill="#2563eb"/>'
        '<line x1="44" y1="44" x2="12" y2="12" stroke="#2563eb" stroke-width="2.6" stroke-linecap="round"/>'
        '<circle cx="10.5" cy="10.5" r="3" fill="#2563eb"/>'
        '<path class="yarn-loop-path" d="M16 30 C16 19, 38 19, 38 30 C38 38, 22 41, 27 47" '
        'stroke="#3b82f6" stroke-width="2.2" stroke-linecap="round" fill="none"/>'
        "</svg>"
        '<h1 class="login-app-title">Knit Industry CRM</h1>'
        '<p class="login-tagline">Every machine, every contact, every visit.</p>'
        "</div>"
    )


def render_login_page(stored_hash: str):
    """Render the login UI, validate submissions, and enforce 5-attempt / 60-second lockout."""
    _load_login_css()

    if "login_failed_attempts" not in st.session_state:
        st.session_state["login_failed_attempts"] = 0
    if "login_lockout_until" not in st.session_state:
        st.session_state["login_lockout_until"] = 0.0
    if "login_last_error" not in st.session_state:
        st.session_state["login_last_error"] = ""
    if "login_shake_nonce" not in st.session_state:
        st.session_state["login_shake_nonce"] = 0

    st.markdown(_brand_svg_html(), unsafe_allow_html=True)

    now = time.time()
    lockout_remaining = int(round(st.session_state["login_lockout_until"] - now))
    is_locked = lockout_remaining > 0

    if not is_locked and st.session_state["login_lockout_until"] > 0:
        st.session_state["login_lockout_until"] = 0.0
        st.session_state["login_failed_attempts"] = 0
        st.session_state["login_last_error"] = ""

    greeting = _dhaka_greeting()

    if st.session_state.get("login_shake_nonce", 0) > 0:
        st.markdown('<div class="login-shake">', unsafe_allow_html=True)

    with st.form("crm_login_form", clear_on_submit=True):
        st.markdown(f'<div class="login-greeting">{html.escape(greeting)}</div>', unsafe_allow_html=True)
        password_input = st.text_input(
            "Password",
            type="password",
            placeholder="Enter access password",
            disabled=is_locked,
        )
        submitted = st.form_submit_button(
            "Sign in",
            type="primary",
            use_container_width=True,
            disabled=is_locked,
        )

    if st.session_state.get("login_shake_nonce", 0) > 0:
        st.markdown("</div>", unsafe_allow_html=True)

    if submitted and not is_locked:
        if verify_password(password_input, stored_hash):
            st.session_state["authenticated"] = True
            st.session_state["login_failed_attempts"] = 0
            st.session_state["login_lockout_until"] = 0.0
            st.session_state["login_last_error"] = ""
            st.session_state["login_shake_nonce"] = 0
            st.markdown(
                '<div class="login-success-card"><strong>Welcome back.</strong><br/>'
                '<span style="font-size:0.85rem;opacity:0.75;">Opening Knit Industry CRM...</span></div>',
                unsafe_allow_html=True,
            )
            time.sleep(0.35)
            st.rerun()
        else:
            time.sleep(0.4)
            st.session_state["login_failed_attempts"] += 1
            st.session_state["login_shake_nonce"] += 1
            if st.session_state["login_failed_attempts"] >= MAX_ATTEMPTS:
                st.session_state["login_lockout_until"] = time.time() + LOCKOUT_SECONDS
                st.session_state["login_last_error"] = ""
            else:
                st.session_state["login_last_error"] = "That password isn't right. Try again."
            st.rerun()

    now_after = time.time()
    rem_after = int(round(st.session_state["login_lockout_until"] - now_after))
    if rem_after > 0:
        st.markdown(
            f'<div class="login-alert" role="alert">Too many attempts. Try again in {rem_after} s.</div>',
            unsafe_allow_html=True,
        )
    elif st.session_state.get("login_last_error"):
        st.markdown(
            f'<div class="login-alert" role="alert">{html.escape(st.session_state["login_last_error"])}</div>',
            unsafe_allow_html=True,
        )

    fact = random.choice(TEXTILE_FACTS)
    st.markdown(
        f'<div class="login-fact-footer">Did you know? {html.escape(fact)}</div>',
        unsafe_allow_html=True,
    )
