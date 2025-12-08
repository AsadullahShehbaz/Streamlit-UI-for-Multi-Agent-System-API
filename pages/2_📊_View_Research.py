import streamlit as st
from utils import get_research_by_id, delete_research

st.set_page_config(page_title="View Research", page_icon="📊")

# Check login
if not st.session_state.get('token'):
    st.error("❌ Please login first!")
    st.stop()

st.title("📊 View Research Details")

# Input for research ID
research_id = st.number_input(
    "Enter Research ID",
    value=st.session_state.get('current_research_id') or 1,
    min_value=1,
    step=1
)

if st.button("🔍 Load Research", type="primary"):
    with st.spinner("Loading..."):
        res, status = get_research_by_id(st.session_state.token, research_id)
    
    if status != 200:
        st.error("❌ Research not found or error occurred")
    else:
        st.success(f"✅ Research {res['id']} Loaded Successfully")
        
        # Display info
        st.markdown(f"### 📝 Query: {res['query']}")
        st.caption(f"**Created:** {res.get('created_at', 'N/A')}")
        st.caption(f"**Status:** {res.get('status', 'N/A')}")
        
        st.divider()
        
        # Final Report
        st.markdown("### 📄 Final Report")
        report = res.get("final_report", "No report available")
        st.markdown(report)
        
        st.divider()
        
        # Actions
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "⬇️ Download Report",
                data=report,
                file_name=f"research_{research_id}.md",
                mime="text/markdown"
            )
        
        with col2:
            if st.button("🗑️ Delete Research", type="secondary"):
                del_result, del_status = delete_research(st.session_state.token, research_id)
                if del_status == 200:
                    st.success("✅ Research deleted successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to delete research")