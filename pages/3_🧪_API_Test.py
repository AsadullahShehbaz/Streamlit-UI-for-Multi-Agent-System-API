import streamlit as st
from utils import get_current_user, get_research_history, health_check
import json
import time

# ------------------------------------
# 🌈 PAGE CONFIGURATION
# ------------------------------------
st.set_page_config(
    page_title="API Test Dashboard",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------
# 🎨 PREMIUM CUSTOM STYLES
# ------------------------------------
st.markdown("""
<style>
/* Import Modern Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Animated Gradient Background */
.main {
    background: linear-gradient(135deg, #0a0e1a 0%, #1a1f3a 25%, #2d1b4e 50%, #1a1f3a 75%, #0a0e1a 100%);
    background-size: 400% 400%;
    animation: gradientShift 20s ease infinite;
    position: relative;
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
        radial-gradient(circle at 80% 70%, rgba(30, 144, 255, 0.15) 0%, transparent 50%);
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
    padding: 2.5rem 2rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 
        0 8px 32px 0 rgba(0, 0, 0, 0.37),
        inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 1;
}

/* Page Title */
.page-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #667eea 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientText 8s ease infinite;
    text-align: center;
    margin-bottom: 1rem;
}

@keyframes gradientText {
    0%, 100% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
}

/* Test Card */
.test-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
    transition: all 0.3s ease;
    animation: slideInUp 0.6s ease-out;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.test-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
}

/* Status Badge */
.status-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0.5rem 0;
}

.status-success {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
}

.status-error {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
}

.status-warning {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
}

/* JSON Display */
.json-container {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 14px;
    padding: 1.5rem;
    margin: 1rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    color: #a5f3fc;
    overflow-x: auto;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);
}

.json-container pre {
    margin: 0;
    color: #a5f3fc;
}

/* Metric Cards */
.metric-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    margin: 0.5rem 0;
}

.metric-label {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
}

/* Enhanced Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 1.5rem !important;
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

/* Health Check Button */
button:has-text("Check API Health") {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 2px solid rgba(102, 126, 234, 0.3) !important;
    border-radius: 12px !important;
    color: white !important;
}

.stSelectbox > div > div:hover {
    border-color: rgba(102, 126, 234, 0.5) !important;
}

/* Success/Error/Warning Messages */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 14px !important;
    backdrop-filter: blur(10px);
    border-left: 4px solid;
    animation: slideInRight 0.5s ease-out;
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.stSuccess {
    background: rgba(34, 197, 94, 0.15) !important;
    border-left-color: #22c55e !important;
}

.stError {
    background: rgba(239, 68, 68, 0.15) !important;
    border-left-color: #ef4444 !important;
}

.stWarning {
    background: rgba(245, 158, 11, 0.15) !important;
    border-left-color: #f59e0b !important;
}

.stInfo {
    background: rgba(59, 130, 246, 0.15) !important;
    border-left-color: #3b82f6 !important;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
    margin: 2.5rem 0;
}

/* Sidebar */
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

/* Spinner */
.stSpinner > div {
    border-top-color: #667eea !important;
}

/* Scrollbar */
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

/* Endpoint Card */
.endpoint-card {
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 14px;
    padding: 1rem;
    margin: 0.5rem 0;
    cursor: pointer;
    transition: all 0.3s ease;
}

.endpoint-card:hover {
    background: rgba(59, 130, 246, 0.2);
    border-color: rgba(59, 130, 246, 0.5);
    transform: translateX(5px);
}

/* Loading Animation */
.loading-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: .5;
    }
}

/* Response Time Badge */
.response-time {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 600;
    background: rgba(168, 85, 247, 0.2);
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.3);
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------
# 🚀 HEADER
# ------------------------------------
st.markdown("<h1 class='page-title'>🧪 API Test Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem;">
        Test and monitor your API endpoints with real-time feedback
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------
# 📊 SIDEBAR - API INFO
# ------------------------------------
with st.sidebar:
    st.markdown("## 🔧 API Configuration")
    
    st.markdown("""
    <div style="background: rgba(102, 126, 234, 0.15); padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
        <div style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">API Status</div>
        <div style="color: #22c55e; font-size: 1.2rem; font-weight: 600;">● Online</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📋 Available Endpoints")
    
    st.markdown("""
    <div class="endpoint-card">
        <div style="color: #22c55e; font-weight: 600;">✓ Health Check</div>
        <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">No auth required</div>
    </div>
    <div class="endpoint-card">
        <div style="color: #3b82f6; font-weight: 600;">🔐 Get Current User</div>
        <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Auth required</div>
    </div>
    <div class="endpoint-card">
        <div style="color: #3b82f6; font-weight: 600;">🔐 Get Research History</div>
        <div style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Auth required</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 💡 Quick Tips")
    st.info("Use this dashboard to test API connectivity and verify endpoint responses.")
    
    if st.button("🏠 Go to Home", use_container_width=True):
        st.switch_page("1_🏠_Home.py")

# ------------------------------------
# 🏥 HEALTH CHECK SECTION
# ------------------------------------
st.markdown("<div class='test-card'>", unsafe_allow_html=True)
st.markdown("### 🏥 Health Check")
st.caption("Verify API server is running and accessible")

col_health1, col_health2 = st.columns([3, 1])

with col_health2:
    health_button = st.button("🔍 Check Health", use_container_width=True)

if health_button:
    start_time = time.time()
    with st.spinner("🔄 Checking API health..."):
        result, status = health_check()
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000, 2)
    
    col_result1, col_result2, col_result3 = st.columns(3)
    
    with col_result1:
        if status == 200:
            st.markdown(f"""
            <div class='metric-card'>
                <div style="font-size: 2rem;">✅</div>
                <div class='metric-value' style='color: #22c55e;'>{status}</div>
                <div class='metric-label'>Status Code</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='metric-card'>
                <div style="font-size: 2rem;">❌</div>
                <div class='metric-value' style='color: #ef4444;'>{status}</div>
                <div class='metric-label'>Status Code</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_result2:
        st.markdown(f"""
        <div class='metric-card'>
            <div style="font-size: 2rem;">⚡</div>
            <div class='metric-value' style='color: #3b82f6;'>{response_time}ms</div>
            <div class='metric-label'>Response Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_result3:
        st.markdown(f"""
        <div class='metric-card'>
            <div style="font-size: 2rem;">📊</div>
            <div class='metric-value' style='color: #a855f7;'>JSON</div>
            <div class='metric-label'>Content Type</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if status == 200:
        st.success("✅ API is healthy and responding!")
    else:
        st.error("❌ API health check failed!")
    
    st.markdown("**Response Data:**")
    st.markdown(f"""
    <div class='json-container'>
        <pre>{json.dumps(result, indent=2)}</pre>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ------------------------------------
# 🔐 AUTHENTICATED ENDPOINTS SECTION
# ------------------------------------
st.markdown("<div class='test-card'>", unsafe_allow_html=True)
st.markdown("### 🔐 Authenticated Endpoints")
st.caption("Test endpoints that require authentication")

if not st.session_state.get('token'):
    st.warning("⚠️ Login required to test authenticated endpoints")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: rgba(245, 158, 11, 0.1); border-radius: 14px; margin-top: 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔒</div>
        <h3 style="color: rgba(255,255,255,0.9);">Authentication Required</h3>
        <p style="color: rgba(255,255,255,0.7);">Please login from the home page to test authenticated endpoints</p>
    </div>
    """, unsafe_allow_html=True)
else:
    col_select, col_button = st.columns([3, 1])
    
    with col_select:
        endpoint = st.selectbox(
            "Choose Endpoint to Test",
            ["Get Current User", "Get Research History"],
            help="Select an API endpoint to test"
        )
    
    with col_button:
        st.markdown("<br>", unsafe_allow_html=True)
        test_button = st.button("🚀 Run Test", type="primary", use_container_width=True)
    
    if test_button:
        start_time = time.time()
        with st.spinner(f"🔄 Testing {endpoint}..."):
            if endpoint == "Get Current User":
                result, status = get_current_user(st.session_state.token)
            else:
                result, status = get_research_history(st.session_state.token)
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)
        
        # Display Results
        col_result1, col_result2, col_result3 = st.columns(3)
        
        with col_result1:
            if status == 200:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style="font-size: 2rem;">✅</div>
                    <div class='metric-value' style='color: #22c55e;'>{status}</div>
                    <div class='metric-label'>Status Code</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style="font-size: 2rem;">❌</div>
                    <div class='metric-value' style='color: #ef4444;'>{status}</div>
                    <div class='metric-label'>Status Code</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_result2:
            st.markdown(f"""
            <div class='metric-card'>
                <div style="font-size: 2rem;">⚡</div>
                <div class='metric-value' style='color: #3b82f6;'>{response_time}ms</div>
                <div class='metric-label'>Response Time</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_result3:
            data_count = len(result) if isinstance(result, list) else 1
            st.markdown(f"""
            <div class='metric-card'>
                <div style="font-size: 2rem;">📦</div>
                <div class='metric-value' style='color: #a855f7;'>{data_count}</div>
                <div class='metric-label'>Records</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if status == 200:
            st.success(f"✅ {endpoint} test successful!")
        else:
            st.error(f"❌ {endpoint} test failed!")
        
        st.markdown(f"**Endpoint:** `{endpoint}`")
        st.markdown(f"**Response Time:** <span class='response-time'>{response_time}ms</span>", unsafe_allow_html=True)
        
        st.markdown("<br>**Response Data:**", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='json-container'>
            <pre>{json.dumps(result, indent=2)}</pre>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------
# 📊 TEST SUMMARY (if tests were run)
# ------------------------------------
if 'test_results' not in st.session_state:
    st.session_state.test_results = []

if st.session_state.get('token'):
    st.divider()
    st.markdown("### 📊 Quick Actions")
    
    col_action1, col_action2, col_action3 = st.columns(3)
    
    with col_action1:
        if st.button("💬 Go to Chat", use_container_width=True):
            st.switch_page("pages/1_💬_Chat_Research.py")
    
    with col_action2:
        if st.button("📊 View Research", use_container_width=True):
            st.switch_page("pages/2_📊_View_Research.py")
    
    with col_action3:
        if st.button("🔄 Refresh Page", use_container_width=True):
            st.rerun()
