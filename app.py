import streamlit as st
from config import SESSION_KEYS
from utils import register_user, login_user, get_research_history

# Page config
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
)

# Initialize session state
for key, default_value in SESSION_KEYS.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# Add registration success flag to session state
if 'registration_success' not in st.session_state:
    st.session_state.registration_success = False

# Main page
st.title("🔬 Multi-Agent Research System")
st.markdown("### Welcome to AI-Powered Research Platform")

# Check if logged in
if st.session_state.token:
    st.success(f"✅ Logged in as: **{st.session_state.user_info['username']}**")
    st.info("👈 Navigate using the sidebar to start researching!")
    
    # Show logout button
    if st.button("🚪 Logout", type="primary"):
        st.session_state.token = None
        st.session_state.user_info = None
        st.session_state.current_research_id = None
        st.session_state.messages = []
        st.session_state.registration_success = False
        st.rerun()
    
    st.divider()
    
    # Show recent research
    st.markdown("### 📚 Recent Research")
    history_data, status = get_research_history(st.session_state.token, limit=5)
    
    if status == 200 and isinstance(history_data, list):
        for item in history_data:
            with st.expander(f"🔍 {item['query'][:50]}..."):
                st.caption(f"**ID:** {item['id']}")
                st.caption(f"**Created:** {item['created_at'][:16]}")
                if st.button("View Details", key=f"view_{item['id']}"):
                    st.session_state.current_research_id = item["id"]
                    st.switch_page("pages/2_📊_View_Research.py")
    else:
        st.info("No research history yet. Start by asking a question!")
else:
    st.info("👈 Please login or register from the sidebar to continue")
    
    # Sidebar for auth
    with st.sidebar:
        st.markdown("### 🔐 Authentication")
        
        # Show registration success message if flag is set
        if st.session_state.registration_success:
            st.success("✅ Registration successful! Please login.")
            st.session_state.registration_success = False  # Reset the flag
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login", type="primary"):
                result, status = login_user(login_username, login_password)
                if status == 200:
                    st.session_state.token = result["access_token"]
                    st.session_state.user_info = {
                        "username": result["username"],
                        "email": result["email"]
                    }
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error(result.get("detail", "Login failed"))
        
        with tab2:
            reg_username = st.text_input("New Username", key="reg_user")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("New Password", type="password", key="reg_pass")
            
            if st.button("Register", type="primary"):
                result, status = register_user(reg_username, reg_email, reg_password)
                if status == 200:
                    # Set success flag and rerun to show message
                    st.session_state.registration_success = True
                    st.rerun()
                else:
                    st.error(result.get("detail", "Registration failed"))
