import streamlit as st
from utils import get_current_user, get_research_history, health_check

st.set_page_config(page_title="API Test", page_icon="🧪")

st.title("🧪 API Test Dashboard")

# Health check (no auth needed)
st.markdown("### 🏥 Health Check")
if st.button("Check API Health"):
    result, status = health_check()
    st.write(f"**Status Code:** {status}")
    st.json(result)

st.divider()

# Auth required tests
if not st.session_state.get('token'):
    st.warning("⚠️ Login required for authenticated endpoints")
    st.stop()

st.markdown("### 🔐 Authenticated Endpoints")

endpoint = st.selectbox(
    "Choose Endpoint",
    ["Get Current User", "Get Research History"]
)

if st.button("🚀 Run Test", type="primary"):
    with st.spinner("Testing..."):
        if endpoint == "Get Current User":
            result, status = get_current_user(st.session_state.token)
        else:
            result, status = get_research_history(st.session_state.token)
    
    st.write(f"**Status Code:** {status}")
    st.json(result)
