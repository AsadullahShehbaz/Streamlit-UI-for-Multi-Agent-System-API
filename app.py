import streamlit as st
from config import SESSION_KEYS
from utils import register_user, login_user, get_research_history

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Researcher Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- PREMIUM GLOBAL STYLES ----------
st.markdown("""
<style>
/* Import Modern Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Animated Gradient Background with Particles Effect */
.main {
    background: linear-gradient(135deg, #0a0e1a 0%, #1a1f3a 25%, #2d1b4e 50%, #1a1f3a 75%, #0a0e1a 100%);
    background-size: 400% 400%;
    animation: gradientShift 20s ease infinite;
    position: relative;
    overflow: hidden;
}

.main::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 30%, rgba(138, 43, 226, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(30, 144, 255, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(255, 20, 147, 0.1) 0%, transparent 50%);
    pointer-events: none;
    animation: pulse 8s ease-in-out infinite;
    z-index: 0;
}

@keyframes gradientShift {
    0%, 100% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
}

@keyframes pulse {
    0%, 100% {opacity: 0.6;}
    50% {opacity: 1;}
}

/* Glass Morphism Container */
.block-container {
    backdrop-filter: blur(20px) saturate(180%);
    background: rgba(255, 255, 255, 0.05);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 
        0 8px 32px 0 rgba(0, 0, 0, 0.37),
        inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 1;
}

/* Animated Neon Title */
.title-anim {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #667eea 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientText 8s ease infinite, float 6s ease-in-out infinite;
    text-align: center;
    letter-spacing: -1px;
    text-shadow: 0 0 40px rgba(102, 126, 234, 0.5);
    margin-bottom: 0.5rem;
}

@keyframes gradientText {
    0%, 100% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
}

@keyframes float {
    0%, 100% {transform: translateY(0px) scale(1);}
    50% {transform: translateY(-10px) scale(1.02);}
}

/* Subtitle with Glow */
.subtitle {
    text-align: center;
    font-size: 1.3rem;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.85);
    margin-bottom: 2rem;
    text-shadow: 0 0 20px rgba(100, 200, 255, 0.4);
    animation: fadeInUp 1s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Enhanced Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.5s;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
}

.stButton > button:active {
    transform: translateY(-1px) scale(1.02) !important;
}

/* Success Messages */
.element-container:has(> .stSuccess) {
    animation: slideInRight 0.5s ease-out;
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Research History Cards */
.research-card {
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.research-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.4s;
}

.research-card:hover::before {
    opacity: 1;
}

.research-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    border-color: rgba(102, 126, 234, 0.5);
}

.research-card h4 {
    color: #fff;
    font-weight: 600;
    font-size: 1.2rem;
    margin-bottom: 0.7rem;
}

.research-card p {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.95rem;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10, 14, 26, 0.95) 0%, rgba(26, 31, 58, 0.95) 100%);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

section[data-testid="stSidebar"] .block-container {
    background: transparent;
    backdrop-filter: none;
    box-shadow: none;
    border: none;
}

/* Input Fields */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
    color: white !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(102, 126, 234, 0.8) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    background: rgba(255, 255, 255, 0.12) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.05);
    padding: 6px;
    border-radius: 14px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.7);
    padding: 0.7rem 1.5rem;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
    margin: 2rem 0;
}

/* Info Box */
.element-container:has(> .stInfo) {
    animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

/* Loading Spinner */
.stSpinner > div {
    border-top-color: #667eea !important;
}

/* Success/Error Messages Enhancement */
.stSuccess, .stError {
    border-radius: 12px !important;
    backdrop-filter: blur(10px);
    border-left: 4px solid;
}

.stSuccess {
    background: rgba(34, 197, 94, 0.15) !important;
    border-left-color: #22c55e !important;
}

.stError {
    background: rgba(239, 68, 68, 0.15) !important;
    border-left-color: #ef4444 !important;
}

/* Logout Button Special Style */
button:has-text("Logout"), button[kind="secondary"] {
    background: rgba(239, 68, 68, 0.2) !important;
    border: 1px solid rgba(239, 68, 68, 0.4) !important;
    color: #fca5a5 !important;
}

button:has-text("Logout"):hover, button[kind="secondary"]:hover {
    background: rgba(239, 68, 68, 0.3) !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4) !important;
}

/* Feature Icons Enhancement */
.feature-icon {
    font-size: 2rem;
    display: inline-block;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 100% {transform: translateY(0);}
    50% {transform: translateY(-5px);}
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #667eea, #764ba2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #764ba2, #667eea);
}
</style>
""", unsafe_allow_html=True)

# ---------- INITIALIZE SESSION STATE ----------
for key, val in SESSION_KEYS.items():
    st.session_state.setdefault(key, val)

st.session_state.setdefault("registration_success", False)

# ---------- HEADER ----------
st.markdown("<h1 class='title-anim'>🤖 AI Researcher Agent</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>✨ Multi-Agent System for Research · Discovery · Automation</div>", unsafe_allow_html=True)


# =====================================================================================
# ------------------------- IF USER IS LOGGED IN --------------------------------------
# =====================================================================================
if st.session_state.token:

    col1, col2 = st.columns([5, 1])
    with col1:
        st.success(f"🎉 Welcome back, **{st.session_state.user_info['username']}**! Ready to discover something amazing?")

    with col2:
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.clear()
            st.rerun()

    st.divider()
    
    # Stats Section
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(16, 185, 129, 0.2)); 
        border-radius: 16px; border: 1px solid rgba(34, 197, 94, 0.3);">
            <h2 style="color: #22c55e; margin: 0; font-size: 2.5rem;">5</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;">Recent Researches</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.2)); 
        border-radius: 16px; border: 1px solid rgba(59, 130, 246, 0.3);">
            <h2 style="color: #3b82f6; margin: 0; font-size: 2.5rem;">∞</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;">AI Powered</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(147, 51, 234, 0.2)); 
        border-radius: 16px; border: 1px solid rgba(168, 85, 247, 0.3);">
            <h2 style="color: #a855f7; margin: 0; font-size: 2.5rem;">24/7</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;">Always Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 📚 Recent Research History")

    history, status = get_research_history(st.session_state.token, limit=5)

    # ----- SHOW HISTORY -----
    if status == 200 and isinstance(history, list) and history:
        for idx, item in enumerate(history):
            st.markdown(
                f"""
                <div class="research-card">
                    <h4>🔍 {item['query'][:85]}{"..." if len(item['query']) > 85 else ""}</h4>
                    <p>📌 Research ID: <code>{item['id']}</code> | 🕒 Created: {item['created_at'][:16].replace('T', ' at ')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
            with col_btn1:
                if st.button("📄 View Details", key=f"view_{item['id']}", use_container_width=True):
                    st.session_state.current_research_id = item["id"]
                    st.switch_page("pages/2_📊_View_Research.py")
            with col_btn2:
                if st.button("🔄 Continue", key=f"continue_{item['id']}", use_container_width=True):
                    st.info("Feature coming soon!")

    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); 
        border-radius: 20px; border: 2px dashed rgba(255, 255, 255, 0.2);">
            <h2 style="color: rgba(255,255,255,0.9); margin-bottom: 1rem;">🎈 Ready to Start Your Research Journey?</h2>
            <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem;">No research history yet. Start exploring from the sidebar to unlock AI-powered insights!</p>
        </div>
        """, unsafe_allow_html=True)



# =====================================================================================
# --------------------------- LOGIN / REGISTER SCREEN ---------------------------------
# =====================================================================================
else:
    # Welcome Screen for Non-Logged Users
    st.markdown("""
    <div style="text-align: center; padding: 2rem; margin: 2rem 0;">
        <p style="font-size: 1.3rem; color: rgba(255,255,255,0.9); line-height: 1.8;">
            Unlock the power of <strong style="color: #667eea;">Artificial Intelligence</strong> to conduct 
            comprehensive research, analyze data, and discover insights in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div style="padding: 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15)); 
        border-radius: 18px; text-align: center; border: 1px solid rgba(102, 126, 234, 0.3); min-height: 200px;">
            <div class="feature-icon">🚀</div>
            <h3 style="color: #fff; margin: 1rem 0 0.5rem 0;">Lightning Fast</h3>
            <p style="color: rgba(255,255,255,0.7);">Get comprehensive research results in seconds with our multi-agent AI system</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f2:
        st.markdown("""
        <div style="padding: 2rem; background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(37, 99, 235, 0.15)); 
        border-radius: 18px; text-align: center; border: 1px solid rgba(59, 130, 246, 0.3); min-height: 200px;">
            <div class="feature-icon">🎯</div>
            <h3 style="color: #fff; margin: 1rem 0 0.5rem 0;">Accurate Results</h3>
            <p style="color: rgba(255,255,255,0.7);">Powered by advanced AI models to deliver precise and reliable information</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f3:
        st.markdown("""
        <div style="padding: 2rem; background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(147, 51, 234, 0.15)); 
        border-radius: 18px; text-align: center; border: 1px solid rgba(168, 85, 247, 0.3); min-height: 200px;">
            <div class="feature-icon">🔒</div>
            <h3 style="color: #fff; margin: 1rem 0 0.5rem 0;">Secure & Private</h3>
            <p style="color: rgba(255,255,255,0.7);">Your data is encrypted and protected with enterprise-grade security</p>
        </div>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #fff; font-weight: 700; font-size: 1.8rem;">🔐 Authentication Portal</h2>
            <p style="color: rgba(255,255,255,0.7);">Access your AI research dashboard</p>
        </div>
        """, unsafe_allow_html=True)

        # Successful registration popup
        if st.session_state.registration_success:
            st.success("🎉 Registration successful! Please login to continue.")
            st.session_state.registration_success = False

        tabs = st.tabs(["🔑 Login", "🆕 Register"])

        # -------- LOGIN TAB --------
        with tabs[0]:
            st.markdown("<br>", unsafe_allow_html=True)
            user = st.text_input("👤 Username", placeholder="Enter your username", key="login_user")
            pwd = st.text_input("🔒 Password", type="password", placeholder="Enter your password", key="login_pwd")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Login", type="primary", use_container_width=True):
                if not user or not pwd:
                    st.error("❌ Please fill in all fields")
                else:
                    with st.spinner("🔄 Authenticating..."):
                        result, status = login_user(user, pwd)
                        if status in [200, 201]:
                            st.session_state.token = result["access_token"]
                            st.session_state.user_info = {
                                "username": result["username"],
                                "email": result["email"]
                            }
                            st.success("✅ Login Successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Please try again.")

        # -------- REGISTER TAB --------
        with tabs[1]:
            st.markdown("<br>", unsafe_allow_html=True)
            new_user = st.text_input("👤 Username", placeholder="Choose a unique username", key="reg_user")
            new_email = st.text_input("📩 Email", placeholder="your.email@example.com", key="reg_email")
            new_pwd = st.text_input("🔑 Password", type="password", placeholder="Create a strong password", key="reg_pwd")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✨ Create Account", type="primary", use_container_width=True):
                if not new_user or not new_email or not new_pwd:
                    st.error("❌ Please fill in all fields")
                elif len(new_pwd) < 6:
                    st.error("❌ Password must be at least 6 characters")
                elif "@" not in new_email:
                    st.error("❌ Please enter a valid email address")
                else:
                    with st.spinner("🔄 Creating your account..."):
                        result, status = register_user(new_user, new_email, new_pwd)
                        if status in [200, 201]:
                            st.session_state.registration_success = True
                            st.rerun()
                        else:
                            st.error("❌ Registration failed. Username or email may already exist.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 12px;">
            <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">
                🔒 Your data is secure and encrypted<br>
                💡 Powered by Advanced AI Technology
            </p>
        </div>
        """, unsafe_allow_html=True)
