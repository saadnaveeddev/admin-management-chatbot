import streamlit as st
import pandas as pd
from user_manager import list_users

def show_user_list():
    st.title("👥 User List Viewer")
    st.markdown("View and manage all users in the system.")
    
    # Get all users
    users = list_users()
    
    if not users:
        st.info("No users found. Use the chatbot to add some users!")
        return
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(users)
    
    # Display user count
    st.metric("Total Users", len(users))
    
    # Search functionality
    search_term = st.text_input("🔍 Search users by name, email, phone, or city:")
    
    if search_term:
        # Filter users based on search term
        filtered_df = df[
            df['name'].str.contains(search_term, case=False, na=False) |
            df['email'].str.contains(search_term, case=False, na=False) |
            df.get('phone', pd.Series(dtype='object')).str.contains(search_term, case=False, na=False) |
            df.get('city', pd.Series(dtype='object')).str.contains(search_term, case=False, na=False)
        ]
    else:
        filtered_df = df
    
    # Display the table
    if len(filtered_df) > 0:
        st.subheader(f"📋 Users ({len(filtered_df)} found)")
        
        # Display as a nice table
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.TextColumn("ID", width="small"),
                "name": st.column_config.TextColumn("Name", width="medium"),
                "email": st.column_config.TextColumn("Email", width="medium"),
                "phone": st.column_config.TextColumn("Phone", width="medium"),
                "city": st.column_config.TextColumn("City", width="medium"),
                "created_at": st.column_config.DatetimeColumn("Created At", width="medium")
            }
        )
        
        # Export functionality
        if st.button("📥 Export to CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="users.csv",
                mime="text/csv"
            )
    else:
        st.warning(f"No users found matching '{search_term}'")
    
    # Refresh button
    if st.button("🔄 Refresh"):
        st.rerun()

if __name__ == "__main__":
    show_user_list()

