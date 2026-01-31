import streamlit as st
from utils import create_research, get_research_history
import base64
import time
import re

# ------------------------------------
# 🌈 PAGE CONFIGURATION
# ------------------------------------
st.set_page_config(
    page_title="AI Research Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------
# 🎨 FIXED CUSTOM STYLES - PROPER Z-INDEX AND VISIBILITY
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

/* FIXED: Background overlay with proper z-index */
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
    z-index: 0 !important;  /* FIXED: Ensure it stays in background */
}

@keyframes gradientShift {
    0%, 100% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
}

@keyframes pulse {
    0%, 100% {opacity: 0.6;}
    50% {opacity: 1;}
}

/* Glass Morphism Container - PROPER Z-INDEX */
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
    z-index: 1 !important;  /* FIXED: Proper layering */
}

/* CRITICAL FIX: Ensure all content is visible */
.stApp {
    position: relative;
    z-index: 1;
}

.stApp > div {
    position: relative;
    z-index: 1;
}

/* Chat messages MUST be visible - SIMPLIFIED AND FIXED */
.stChatMessage {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 18px !important;
    padding: 1.2rem !important;
    margin-bottom: 1rem !important;
    animation: slideInUp 0.4s ease-out !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    z-index: 10 !important;  /* FIXED: Proper stacking */
}

.stChatMessage:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    border-color: rgba(102, 126, 234, 0.4) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
}

/* Animated Header */
.chat-header {
    text-align: center;
    margin-bottom: 2rem;
    animation: fadeInDown 0.8s ease-out;
    position: relative;
    z-index: 2;
}

.chat-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #667eea 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientText 8s ease infinite;
    margin-bottom: 0.5rem;
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes gradientText {
    0%, 100% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* User Message Content - FIXED VISIBILITY */
[data-testid="stChatMessageContent"] {
    color: rgba(255, 255, 255, 0.95) !important;
    line-height: 1.7;
    position: relative;
    z-index: 11 !important;
}

/* Ensure text is visible */
.stChatMessage p,
.stChatMessage div,
.stChatMessage span {
    color: rgba(255, 255, 255, 0.95) !important;
    position: relative;
    z-index: 11;
}

/* ============================================
   TABLE AND LINK STYLING - PROPER WRAPPING
   ============================================ */

/* Force tables to be responsive */
.stChatMessage table {
    display: block !important;
    width: 100% !important;
    overflow-x: auto !important;
    border-collapse: collapse !important;
    font-size: 0.9rem !important;
    position: relative;
    z-index: 11;
    background: rgba(0, 0, 0, 0.3) !important;
    border-radius: 8px;
}

.stChatMessage thead,
.stChatMessage tbody {
    display: table !important;
    width: 100% !important;
    table-layout: fixed !important;
}

.stChatMessage tr {
    display: table-row !important;
    width: 100% !important;
}

.stChatMessage th,
.stChatMessage td {
    display: table-cell !important;
    padding: 0.75rem !important;
    vertical-align: top !important;
    word-wrap: break-word !important;
    word-break: break-word !important;
    overflow-wrap: break-word !important;
    hyphens: auto !important;
    white-space: normal !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.stChatMessage th {
    background: rgba(102, 126, 234, 0.2) !important;
    font-weight: 600;
}

/* Specific fix for link column */
.stChatMessage td:last-child,
.stChatMessage th:last-child {
    min-width: 200px !important;
    max-width: 300px !important;
    width: 25% !important;
}

/* Force all links to wrap properly */
.stChatMessage a {
    display: inline !important;
    word-wrap: break-word !important;
    word-break: break-all !important;
    overflow-wrap: anywhere !important;
    white-space: normal !important;
    line-height: 1.6 !important;
    color: #60a5fa !important;
    text-decoration: none !important;
    hyphens: auto !important;
    max-width: 100% !important;
    position: relative;
    z-index: 12;
}

.stChatMessage a:hover {
    color: #93c5fd !important;
    text-decoration: underline !important;
}

.stChatMessage td a {
    font-size: 0.85rem !important;
}

/* Ensure markdown container doesn't restrict width */
.stChatMessage [data-testid="stMarkdownContainer"] {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    position: relative;
    z-index: 11;
}

/* Additional wrapper fix */
.stChatMessage > div {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: auto !important;
}

/* Scrollbar for tables */
.stChatMessage table::-webkit-scrollbar {
    height: 8px;
}

.stChatMessage table::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}

.stChatMessage table::-webkit-scrollbar-thumb {
    background: rgba(102, 126, 234, 0.5);
    border-radius: 10px;
}

.stChatMessage table::-webkit-scrollbar-thumb:hover {
    background: rgba(102, 126, 234, 0.7);
}

/* Chat Input - ENSURE VISIBILITY */
.stChatInput {
    position: sticky;
    bottom: 0;
    z-index: 100 !important;  /* FIXED: High z-index for input */
    padding: 1rem 0;
    background: linear-gradient(to top, rgba(10, 14, 26, 0.95), transparent);
}

.stChatInput > div {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 2px solid rgba(102, 126, 234, 0.3) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}

.stChatInput > div:focus-within {
    border-color: rgba(102, 126, 234, 0.8) !important;
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2) !important;
    background: rgba(255, 255, 255, 0.12) !important;
}

.stChatInput textarea {
    color: white !important;
    font-size: 1rem !important;
}

.stChatInput textarea::placeholder {
    color: rgba(255, 255, 255, 0.5) !important;
}

/* Enhanced Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 1.2rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    position: relative;
    overflow: hidden;
    z-index: 10;
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
    transform: translateY(-2px) scale(1.03) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10, 14, 26, 0.95) 0%, rgba(26, 31, 58, 0.95) 100%);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 50;
}

section[data-testid="stSidebar"] .block-container {
    background: transparent;
    backdrop-filter: none;
    box-shadow: none;
    border: none;
}

/* History Item Styling */
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(102, 126, 234, 0.15) !important;
    border: 1px solid rgba(102, 126, 234, 0.3) !important;
    text-align: left !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(102, 126, 234, 0.25) !important;
    border-color: rgba(102, 126, 234, 0.5) !important;
}

/* Code Blocks - Enhanced Interactive Style */
.stChatMessage pre {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95)) !important;
    border: 1px solid rgba(102, 126, 234, 0.3) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    margin: 1rem 0 !important;
    overflow-x: auto !important;
    position: relative !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    font-family: 'Fira Code', 'Monaco', 'Courier New', monospace !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
    z-index: 11;
}

.stChatMessage pre:hover {
    border-color: rgba(102, 126, 234, 0.6) !important;
    box-shadow: 0 6px 25px rgba(102, 126, 234, 0.2) !important;
}

/* Code inside pre */
.stChatMessage pre code {
    background: transparent !important;
    color: #e2e8f0 !important;
    padding: 0 !important;
    border-radius: 0 !important;
    font-size: inherit !important;
    display: block !important;
}

/* Inline code (not in pre) */
.stChatMessage code {
    background: rgba(102, 126, 234, 0.2) !important;
    color: #c084fc !important;
    padding: 0.2rem 0.5rem !important;
    border-radius: 6px !important;
    font-family: 'Monaco', 'Courier New', monospace !important;
    font-size: 0.9em !important;
    border: 1px solid rgba(102, 126, 234, 0.3) !important;
}

.stChatMessage :not(pre) > code {
    white-space: nowrap !important;
}

/* Caption Text */
.caption {
    color: rgba(255, 255, 255, 0.6) !important;
    font-size: 0.85rem;
    margin-top: 0.3rem;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
    margin: 1.5rem 0;
}

/* Success/Error Messages */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 14px !important;
    backdrop-filter: blur(10px);
    border-left: 4px solid;
    animation: slideInRight 0.5s ease-out;
    z-index: 20;
    position: relative;
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

/* Section Headers in Messages */
.stChatMessage h2, .stChatMessage h3 {
    color: #c084fc !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}

.stChatMessage h2 {
    font-size: 1.5rem !important;
}

.stChatMessage h3 {
    font-size: 1.2rem !important;
}

/* Sidebar Headers */
section[data-testid="stSidebar"] h2 {
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
    margin-bottom: 1rem !important;
}

section[data-testid="stSidebar"] h3 {
    color: rgba(255, 255, 255, 0.9) !important;
    font-weight: 600 !important;
    margin-top: 1.5rem !important;
}

/* Caption in Sidebar */
section[data-testid="stSidebar"] .caption {
    background: rgba(255, 255, 255, 0.05);
    padding: 0.4rem 0.6rem;
    border-radius: 8px;
    font-size: 0.75rem;
    margin-bottom: 0.5rem;
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

/* Responsive Design */
@media (max-width: 768px) {
    .chat-title {
        font-size: 2rem !important;
    }
    
    .stChatMessage table {
        font-size: 0.8rem !important;
    }
    
    .stChatMessage th,
    .stChatMessage td {
        padding: 0.5rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------
# 🔐 LOGIN CHECK
# ------------------------------------
if not st.session_state.get('token'):
    st.error("🔒 Authentication Required")
    st.warning("Please login from the home page to access the AI Research Assistant")
    if st.button("🏠 Go to Home", type="primary"):
        st.switch_page("app.py")
    st.stop()

# ------------------------------------
# 🚀 HEADER
# ------------------------------------
st.markdown("""
<div class="chat-header">
    <div class="chat-title">💬 AI Research Agent</div>
    <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem; margin: 0;">
        Ask research questions and generate structured reports powered by AI
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------
# 📚 SIDEBAR (Research History)
# ------------------------------------
with st.sidebar:
    st.markdown("## 📜 Research History")
    st.caption("Quick access to your previous research")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    
    st.markdown("---")

    history_data, status = get_research_history(st.session_state.token, limit=20)

    if status == 200 and isinstance(history_data, list):
        if history_data:
            for idx, item in enumerate(history_data):
                with st.container():
                    if st.button(
                        f"🔍 {item['query'][:35]}...", 
                        key=f"hist_{item['id']}", 
                        use_container_width=True,
                        help=f"View research: {item['query']}"
                    ):
                        st.session_state.current_research_id = item["id"]
                        st.switch_page("pages/2_📊_View_Research.py")
                    
                    st.markdown(
                        f"<div class='caption'>🆔 {str(item['id'])} • 🕒 {item['created_at'][5:16].replace('T', ' ')}</div>",
                        unsafe_allow_html=True
                    )
                    
                    if idx < len(history_data) - 1:
                        st.markdown("---")
        else:
            st.info("💡 No research history yet. Start a conversation below!")
    else:
        st.warning("⚠️ Unable to load history")

    # ------------------------------------
    # 📤 EXPORT OPTIONS
    # ------------------------------------
    st.markdown("---")
    st.subheader("📁 Export Options")
    st.caption("Save your research conversation")

    if "messages" in st.session_state and st.session_state.messages:
        chat_text = "\n\n".join([
            f"**{msg['role'].upper()}:**\n{msg['content']}" 
            for msg in st.session_state.messages
        ])
        
        # Download MD
        st.download_button(
            label="⬇️ Download as Markdown",
            data=chat_text,
            file_name=f"research_chat_{time.strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True,
            help="Save conversation as a markdown file"
        )
    else:
        st.info("💬 Start chatting to enable export")

    # ------------------------------------
    # 🧹 CLEAR CHAT
    # ------------------------------------
    st.markdown("---")
    if st.button("🧹 Clear Chat", use_container_width=True, help="Remove all messages"):
        st.session_state.messages = []
        st.success("✨ Chat cleared!")
        st.rerun()

# ------------------------------------
# 🗂️ MESSAGE INITIALIZATION
# ------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Message
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); 
    border-radius: 20px; border: 2px dashed rgba(102, 126, 234, 0.3); margin: 2rem 0; position: relative; z-index: 5;">
        <h2 style="color: rgba(255,255,255,0.95); margin-bottom: 1rem;">👋 Welcome to AI Research Assistant!</h2>
        <p style="color: rgba(255,255,255,0.75); font-size: 1.1rem; line-height: 1.8;">
            I'm here to help you with comprehensive research on any topic.<br>
            <strong style="color: #667eea;">Just ask a question below</strong> and I'll analyze, research, and generate detailed reports.
        </p>
        <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 200px; max-width: 250px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚀</div>
                <div style="color: rgba(255,255,255,0.9); font-weight: 600;">Fast Results</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">Get insights in seconds</div>
            </div>
            <div style="flex: 1; min-width: 200px; max-width: 250px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                <div style="color: rgba(255,255,255,0.9); font-weight: 600;">Accurate Analysis</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">AI-powered precision</div>
            </div>
            <div style="flex: 1; min-width: 200px; max-width: 250px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <div style="color: rgba(255,255,255,0.9); font-weight: 600;">Structured Reports</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">Well-organized findings</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------
# 💬 SHOW CHAT HISTORY - FIXED
# ------------------------------------
chat_container = st.container()
with chat_container:
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"], avatar="🧑‍💼" if msg["role"] == "user" else "🤖"):
            content = msg["content"]
            
            # Check if content has code blocks
            if "```" in content:
                parts = content.split("```")
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        # Regular text
                        if part.strip():
                            st.markdown(part)
                    else:
                        # Code block
                        lines = part.split('\n', 1)
                        language = lines[0].strip() if len(lines) > 0 else ""
                        code_content = lines[1] if len(lines) > 1 else part
                        
                        # Use streamlit's code component for better display
                        if language and language.isalpha():
                            st.code(code_content, language=language)
                        else:
                            st.code(code_content, language="python")
            else:
                st.markdown(content)

# ------------------------------------
# 📥 USER INPUT
# ------------------------------------
user_query = st.chat_input("💭 Ask anything about your research topic...", key="chat_input")

if user_query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Display user message
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(user_query)

    # Generate AI response
    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        
        # Show loading with clean message
        response_placeholder.info("🔬 Researching your topic... Please wait.")
        
        with st.spinner("Analyzing documents and forming conclusions..."):
            result, status = create_research(st.session_state.token, user_query, max_iterations=2)
        
        if status != 200:
            error_msg = f"""
### ❌ Research Error

**Error Details:** {result.get('detail', 'Unknown error occurred')}

Please try again or contact support if the issue persists.
"""
            response_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            # Success - Display clean report without HTML tags
            final_report = result.get('final_report', 'No report generated')
            
            # Remove the status-badge div if it exists in the report
            if '<div class="status-badge">' in final_report:
                final_report = re.sub(r'<div class="status-badge">.*?</div>', '', final_report, flags=re.DOTALL)
            
            report_md = f"""
### ✅ Research Completed Successfully

**Research ID:** `{result['id']}`  
**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

## 📄 Final Report

{final_report}

---

*💡 Tip: You can view more details by clicking on this research in the sidebar history.*
"""
            response_placeholder.markdown(report_md)
            st.session_state.messages.append({"role": "assistant", "content": report_md})
            st.session_state.current_research_id = result["id"]
            
            # Show success message
            st.success("✨ Research saved to history!")
            
            # Auto-scroll to bottom
            st.rerun()

# ------------------------------------
# 📊 CHAT STATS (Bottom Info)
# ------------------------------------
if st.session_state.messages:
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: rgba(102, 126, 234, 0.15); border-radius: 12px;">
            <div style="font-size: 1.5rem; color: #667eea; font-weight: 700;">{len(st.session_state.messages)}</div>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">Total Messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: rgba(34, 197, 94, 0.15); border-radius: 12px;">
            <div style="font-size: 1.5rem; color: #22c55e; font-weight: 700;">{user_msgs}</div>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">Your Questions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        ai_msgs = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: rgba(168, 85, 247, 0.15); border-radius: 12px;">
            <div style="font-size: 1.5rem; color: #a855f7; font-weight: 700;">{ai_msgs}</div>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">AI Responses</div>
        </div>
        """, unsafe_allow_html=True)
