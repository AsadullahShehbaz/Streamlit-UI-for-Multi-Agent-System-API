import streamlit as st
from utils import get_research_by_id, delete_research
import time

# ------------------------------------
# 🌈 PAGE CONFIGURATION
# ------------------------------------
st.set_page_config(
    page_title="View Research",
    page_icon="📊",
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
    animation: gradientText 8s ease infinite, float 6s ease-in-out infinite;
    text-align: center;
    margin-bottom: 1rem;
}

@keyframes gradientText {
    0%, 100% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
}

@keyframes float {
    0%, 100% {transform: translateY(0px);}
    50% {transform: translateY(-8px);}
}

/* Search Card */
.search-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

.search-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
}

/* Research Details Card */
.details-card {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(37, 99, 235, 0.15));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
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

/* Report Container */
.report-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 18px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2);
}

.report-container h1, .report-container h2, .report-container h3 {
    color: #c084fc !important;
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
}

.report-container h1 {
    font-size: 2rem !important;
    border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    padding-bottom: 0.5rem;
}

.report-container h2 {
    font-size: 1.6rem !important;
}

.report-container h3 {
    font-size: 1.3rem !important;
}

.report-container p {
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.8;
    margin-bottom: 1rem;
}

.report-container ul, .report-container ol {
    color: rgba(255, 255, 255, 0.85);
    line-height: 1.8;
    margin-left: 1.5rem;
}

.report-container code {
    background: rgba(102, 126, 234, 0.2);
    color: #c084fc;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    font-family: 'Monaco', 'Courier New', monospace;
}

.report-container blockquote {
    border-left: 4px solid #667eea;
    padding-left: 1rem;
    margin: 1rem 0;
    color: rgba(255, 255, 255, 0.8);
    font-style: italic;
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

.status-completed {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
}

.status-processing {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    animation: pulse 2s infinite;
}

.status-failed {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
}

@keyframes pulse {
    0%, 100% {
        box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7);
    }
    50% {
        box-shadow: 0 0 0 10px rgba(245, 158, 11, 0);
    }
}

/* Info Box */
.info-box {
    background: rgba(59, 130, 246, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 14px;
    padding: 1.2rem;
    margin: 1rem 0;
}

.info-box-icon {
    font-size: 1.5rem;
    margin-right: 0.5rem;
}

.info-box-label {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
}

.info-box-value {
    color: white;
    font-size: 1.1rem;
    font-weight: 600;
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

/* Download Button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
}

.stDownloadButton > button:hover {
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.6) !important;
}

/* Delete Button */
button[kind="secondary"] {
    background: linear-gradient(135deg, #ef4444, #dc2626) !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4) !important;
}

button[kind="secondary"]:hover {
    box-shadow: 0 8px 25px rgba(239, 68, 68, 0.6) !important;
}

/* Number Input */
.stNumberInput > div > div > input {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 2px solid rgba(102, 126, 234, 0.3) !important;
    border-radius: 12px !important;
    color: white !important;
    padding: 0.8rem 1rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
}

.stNumberInput > div > div > input:focus {
    border-color: rgba(102, 126, 234, 0.8) !important;
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2) !important;
    background: rgba(255, 255, 255, 0.12) !important;
}

/* Success/Error Messages */
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

.stInfo {
    background: rgba(59, 130, 246, 0.15) !important;
    border-left-color: #3b82f6 !important;
}

.stWarning {
    background: rgba(245, 158, 11, 0.15) !important;
    border-left-color: #f59e0b !important;
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

/* Action Cards */
.action-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.action-card:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
    border-radius: 20px;
    border: 2px dashed rgba(102, 126, 234, 0.3);
    margin: 2rem 0;
}

.empty-state-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 100% {transform: translateY(0);}
    50% {transform: translateY(-10px);}
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------
# 🔐 LOGIN CHECK
# ------------------------------------
if not st.session_state.get('token'):
    st.error("🔒 Authentication Required")
    st.warning("Please login from the home page to view research details")
    if st.button("🏠 Go to Home", type="primary"):
        st.switch_page("app.py")
    st.stop()

# ------------------------------------
# 🚀 HEADER
# ------------------------------------
st.markdown("<h1 class='page-title'>📊 View Research Details</h1>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem;">
        Access and manage your AI-generated research reports
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------
# 🔍 SIDEBAR NAVIGATION
# ------------------------------------
with st.sidebar:
    st.markdown("## 🧭 Quick Navigation")
    
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("1_🏠_Home.py")
    
    if st.button("💬 New Research", use_container_width=True):
        st.switch_page("pages/1_💬_Chat_Research.py")
    
    st.markdown("---")
    st.markdown("## 💡 Tips")
    st.info("Enter a research ID to view detailed reports and manage your research data.")
    
    st.markdown("---")
    st.markdown("## 🎯 Features")
    st.markdown("""
    - 📄 View full reports
    - ⬇️ Download as Markdown
    - 🗑️ Delete research
    - 📊 Track research status
    """)

# ------------------------------------
# 🔍 SEARCH SECTION
# ------------------------------------
st.markdown("<div class='search-card'>", unsafe_allow_html=True)
st.markdown("### 🔍 Search Research")

col1, col2 = st.columns([3, 1])

with col1:
    research_id = st.number_input(
        "Enter Research ID",
        value=st.session_state.get('current_research_id') or 1,
        min_value=1,
        step=1,
        help="Enter the ID of the research you want to view"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    load_button = st.button("🔍 Load Research", type="primary", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------
# 📊 LOAD AND DISPLAY RESEARCH
# ------------------------------------
if load_button:
    with st.spinner("🔄 Loading research data..."):
        res, status = get_research_by_id(st.session_state.token, research_id)
    
    if status != 200:
        st.error("❌ Research not found or an error occurred")
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-state-icon'>🔍</div>
            <h3 style='color: rgba(255,255,255,0.9);'>Research Not Found</h3>
            <p style='color: rgba(255,255,255,0.7);'>
                The research ID you entered doesn't exist or you don't have access to it.<br>
                Please check the ID and try again.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success(f"✅ Research #{res['id']} loaded successfully!")
        st.balloons()
        
        # Store in session state
        st.session_state.loaded_research = res
        
        # ------------------------------------
        # 📋 RESEARCH HEADER INFO
        # ------------------------------------
        st.markdown("<div class='details-card'>", unsafe_allow_html=True)
        
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.markdown(f"""
            <div class='info-box'>
                <div class='info-box-icon'>📝</div>
                <div class='info-box-label'>Research Query</div>
                <div class='info-box-value'>{res['query']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info2:
            status_class = "status-completed" if res.get('status') == 'completed' else "status-processing"
            st.markdown(f"""
            <div class='info-box'>
                <div class='info-box-icon'>📊</div>
                <div class='info-box-label'>Status</div>
                <div class='info-box-value'>
                    <span class='status-badge {status_class}'>{res.get('status', 'N/A').upper()}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        col_info3, col_info4 = st.columns(2)
        
        with col_info3:
            st.markdown(f"""
            <div class='info-box'>
                <div class='info-box-icon'>🆔</div>
                <div class='info-box-label'>Research ID</div>
                <div class='info-box-value'>{res['id']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info4:
            created_date = res.get('created_at', 'N/A')
            if created_date != 'N/A':
                created_date = created_date.replace('T', ' at ')[:19]
            st.markdown(f"""
            <div class='info-box'>
                <div class='info-box-icon'>🕒</div>
                <div class='info-box-label'>Created At</div>
                <div class='info-box-value'>{created_date}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.divider()
        
        # ------------------------------------
        # 📄 FINAL REPORT
        # ------------------------------------
        st.markdown("### 📄 Final Research Report")
        
        report = res.get("final_report", "No report available")
        
        if report and report != "No report available":
            st.markdown(f"<div class='report-container'>{report}</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ No report has been generated for this research yet.")
        
        st.divider()
        
        # ------------------------------------
        # 🎬 ACTION BUTTONS
        # ------------------------------------
        st.markdown("### 🎬 Actions")
        
        col_action1, col_action2, col_action3 = st.columns(3)
        
        with col_action1:
            st.markdown("<div class='action-card'>", unsafe_allow_html=True)
            st.markdown("**⬇️ Download Report**")
            st.caption("Save as Markdown file")
            st.download_button(
                "Download .md",
                data=report,
                file_name=f"research_{research_id}_{time.strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True,
                help="Download the full report as a Markdown file"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_action2:
            st.markdown("<div class='action-card'>", unsafe_allow_html=True)
            st.markdown("**💬 Continue Research**")
            st.caption("Ask more questions")
            if st.button("Open Chat", use_container_width=True, help="Continue this research in chat"):
                st.session_state.current_research_id = research_id
                st.switch_page("pages/1_💬_Chat_Research.py")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_action3:
            st.markdown("<div class='action-card'>", unsafe_allow_html=True)
            st.markdown("**🗑️ Delete Research**")
            st.caption("Permanently remove")
            if st.button("Delete", type="secondary", use_container_width=True, help="Delete this research permanently"):
                with st.spinner("Deleting research..."):
                    del_result, del_status = delete_research(st.session_state.token, research_id)
                if del_status == 200:
                    st.success("✅ Research deleted successfully!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Failed to delete research. Please try again.")
            st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------
# 📊 SHOW LOADED RESEARCH (IF EXISTS)
# ------------------------------------
elif 'loaded_research' in st.session_state:
    res = st.session_state.loaded_research
    
    # Display the same information as above
    st.info("💡 Showing previously loaded research. Enter a new ID above to load different research.")
    
    # ------------------------------------
    # 📋 RESEARCH HEADER INFO
    # ------------------------------------
    st.markdown("<div class='details-card'>", unsafe_allow_html=True)
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown(f"""
        <div class='info-box'>
            <div class='info-box-icon'>📝</div>
            <div class='info-box-label'>Research Query</div>
            <div class='info-box-value'>{res['query']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        status_class = "status-completed" if res.get('status') == 'completed' else "status-processing"
        st.markdown(f"""
        <div class='info-box'>
            <div class='info-box-icon'>📊</div>
            <div class='info-box-label'>Status</div>
            <div class='info-box-value'>
                <span class='status-badge {status_class}'>{res.get('status', 'N/A').upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col_info3, col_info4 = st.columns(2)
    
    with col_info3:
        st.markdown(f"""
        <div class='info-box'>
            <div class='info-box-icon'>🆔</div>
            <div class='info-box-label'>Research ID</div>
            <div class='info-box-value'>{res['id']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info4:
        created_date = res.get('created_at', 'N/A')
        if created_date != 'N/A':
            created_date = created_date.replace('T', ' at ')[:19]
        st.markdown(f"""
        <div class='info-box'>
            <div class='info-box-icon'>🕒</div>
            <div class='info-box-label'>Created At</div>
            <div class='info-box-value'>{created_date}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # ------------------------------------
    # 📄 FINAL REPORT
    # ------------------------------------
    st.markdown("### 📄 Final Research Report")
    
    report = res.get("final_report", "No report available")
    
    if report and report != "No report available":
        st.markdown(f"<div class='report-container'>{report}</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ No report has been generated for this research yet.")
    
    st.divider()
    
    # ------------------------------------
    # 🎬 ACTION BUTTONS
    # ------------------------------------
    st.markdown("### 🎬 Actions")
    
    col_action1, col_action2, col_action3 = st.columns(3)
    
    with col_action1:
        st.markdown("<div class='action-card'>", unsafe_allow_html=True)
        st.markdown("**⬇️ Download Report**")
        st.caption("Save as Markdown file")
        st.download_button(
            "Download .md",
            data=report,
            file_name=f"research_{res['id']}_{time.strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True,
            help="Download the full report as a Markdown file"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_action2:
        st.markdown("<div class='action-card'>", unsafe_allow_html=True)
        st.markdown("**💬 Continue Research**")
        st.caption("Ask more questions")
        if st.button("Open Chat", use_container_width=True, help="Continue this research in chat"):
            st.session_state.current_research_id = res['id']
            st.switch_page("pages/1_💬_Chat_Research.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_action3:
        st.markdown("<div class='action-card'>", unsafe_allow_html=True)
        st.markdown("**🗑️ Delete Research**")
        st.caption("Permanently remove")
        if st.button("Delete", type="secondary", use_container_width=True, help="Delete this research permanently"):
            with st.spinner("Deleting research..."):
                del_result, del_status = delete_research(st.session_state.token, res['id'])
            if del_status == 200:
                st.success("✅ Research deleted successfully!")
                st.balloons()
                time.sleep(2)
                if 'loaded_research' in st.session_state:
                    del st.session_state.loaded_research
                st.rerun()
            else:
                st.error("❌ Failed to delete research. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)
