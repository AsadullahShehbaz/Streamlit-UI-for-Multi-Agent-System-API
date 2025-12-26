import streamlit as st
from config import SESSION_KEYS
from utils import register_user, login_user, get_research_history

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Researcher Agent",
    page_icon="🤖",
    layout="wide",
)

# ---------- GLOBAL STYLES ----------
st.markdown("""
<style>
/* Gradient Background */
.main {
    background: linear-gradient(135deg, #0d0f16, #1b2333, #26344d);
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
}
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glass Cards */
.block-container {
    backdrop-filter: blur(18px);
    background: rgba(255,255,255,0.08);
    border-radius:20px;
    padding: 2.5rem;
    box-shadow: 0 0 25px rgba(0,0,0,0.35);
}

/* Buttons */
button[kind="primary"] {
    border-radius: 12px !important;
    padding: 0.6rem 1.1rem !important;
    font-size: 1rem !important;
}

/* Title Animation */
.title-anim {
    font-size: 3rem;
    font-weight: 700;
    background: -webkit-linear-gradient(#7dd3fc, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: float 4s ease-in-out infinite;
}
@keyframes float {
    0% {transform: translateY(0px);}
    50% {transform: translateY(-6px);}
    100% {transform: translateY(0px);}
}
</style>
""", unsafe_allow_html=True)

# ---------- INITIALIZE SESSION STATE ----------
for key, val in SESSION_KEYS.items():
    st.session_state.setdefault(key, val)

st.session_state.setdefault("registration_success", False)


# ---------- HEADER ----------
st.markdown("<h1 class='title-anim'>🤖 AI Researcher Agent</h1>", unsafe_allow_html=True)
st.markdown("### *Your personal multi-agent system for research, discovery & insights*")


# =====================================================================================
# ------------------------- IF USER IS LOGGED IN --------------------------------------
# =====================================================================================
if st.session_state.token:

    col1, col2 = st.columns([6,1])
    with col1:
        st.success(f"🎉 Welcome, **{st.session_state.user_info['username']}**")
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.experimental_rerun()

    st.divider()
    st.markdown("## 📚 Recent Research History")

    history, status = get_research_history(st.session_state.token, limit=5)

    if status == 200 and isinstance(history, list) and history:
        for item in history:
            with st.container():
                st.markdown(
                    f"""
                    <div style="padding:1rem; margin-bottom:1rem; border-radius:16px;
                    background:rgba(255,255,255,0.15); backdrop-filter:blur(10px);">
                    <h4>🔍 {item['query'][:70]}...</h4>
                    <p>📌 ID: {item['id']} | 🕒 {item['created_at'][:16]}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
                if st.button("📄 View Research", key=f"view_{item['id']}"):
                    st.session_state.current_research_id = item["id"]
                    st.switch_page("pages/2_📊_View_Research.py")
    else:
        st.info("🎈 No research yet — start with a question in the sidebar!")


# =====================================================================================
# --------------------------- LOGIN / REGISTER SCREEN ---------------------------------
# =====================================================================================
else:
    with st.sidebar:
        st.markdown("## 🔐 Authentication")

        if st.session_state.registration_success:
            st.success("🎉 Registration successful! Please login.")
            st.session_state.registration_success = False  

        tabs = st.tabs(["🔑 Login", "🆕 Register"])

        # -------- LOGIN TAB --------
        with tabs[0]:
            user = st.text_input("👤 Username")
            pwd = st.text_input("🔒 Password", type="password")

            if st.button("Login", use_container_width=True):
                result, status = login_user(user, pwd)
                if status in [200, 201]:
                    st.session_state.token = result["access_token"]
                    st.session_state.user_info = {"username": result["username"], "email": result["email"]}
                    st.success("🚀 Logged in successfully!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Invalid credentials")

        # -------- REGISTER TAB --------
        with tabs[1]:
            new_user = st.text_input("👤 Create Username")
            new_email = st.text_input("📩 Email")
            new_pwd = st.text_input("🔑 Create Password", type="password")

            if st.button("Register", use_container_width=True):
                result, status = register_user(new_user, new_email, new_pwd)
                if status in [200, 201]:
                    st.session_state.registration_success = True
                    st.experimental_rerun()
                else:
                    st.error("❌ Registration failed. Try again.")

