import streamlit as st
from utils import create_research, get_research_history

st.set_page_config(page_title="Chat Research", page_icon="💬")

# Check login
if not st.session_state.get('token'):
    st.error("❌ Please login first!")
    st.stop()

st.title("💬 Chat with AI Researcher")

# Sidebar - Research History
with st.sidebar:
    st.markdown("### 📚 Research History")
    
    if st.button("🔄 Refresh History"):
        st.rerun()
    
    history_data, status = get_research_history(st.session_state.token, limit=20)
    
    if status == 200 and isinstance(history_data, list):
        for item in history_data:
            if st.button(f"{item['query'][:30]}...", key=f"hist_{item['id']}"):
                st.session_state.current_research_id = item["id"]
                st.switch_page("pages/2_📊_View_Research.py")
            st.caption(f"ID: {item['id']} | {item['created_at'][:16]}")
            st.markdown("---")

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_query = st.chat_input("Ask your research question...")

if user_query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🔬 Researching..."):
            result, status = create_research(st.session_state.token, user_query, max_iterations=2)
        
        if status != 200:
            error_msg = f"❌ Error: {result.get('detail', 'Unknown error')}"
            st.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            reply = f"""
### ✅ Research Completed  
**Research ID:** {result['id']}  

#### 📄 Final Report  
{result.get('final_report', 'No report generated')}
            """
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.current_research_id = result["id"]

# Clear chat button
st.divider()
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()