import streamlit as st
import json
from datetime import datetime
import uuid
from user_manager import add_user, get_user, update_user, delete_user, list_users
from gemini_integration import get_gemini_response

# Page configuration
st.set_page_config(
    page_title="User Management Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def process_command(command):
    """Process natural language commands using Gemini API"""
    # Create a prompt to help Gemini understand what we want
    prompt = f"""
    You are a user management assistant. Analyze the following command and determine what action to take.
    
    Command: "{command}"
    
    Available actions:
    1. ADD_USER - Add a new user (requires name, email, and optionally age, role)
    2. GET_USER - Get user information (requires name or ID)
    3. UPDATE_USER - Update user information (requires user identifier and new data)
    4. DELETE_USER - Delete a user (requires name or ID)
    5. LIST_USERS - List all users
    6. HELP - Show available commands
    
    Please respond with:
    - ACTION: [action name]
    - PARAMETERS: [extracted parameters as key-value pairs]
    - RESPONSE: [friendly response to the user]
    
    If the command is unclear or missing required information, ask for clarification.
    """
    
    try:
        response = get_gemini_response(prompt)
        return response
    except Exception as e:
        return f"Sorry, I couldn't process your command. Error: {str(e)}"

def execute_action(gemini_response, original_command):
    """Execute the action based on Gemini's analysis"""
    try:
        # Simple parsing of Gemini response
        lines = gemini_response.split('\n')
        action = None
        parameters = {}
        
        for line in lines:
            if line.startswith('ACTION:'):
                action = line.replace('ACTION:', '').strip()
            elif line.startswith('PARAMETERS:'):
                # Simple parameter extraction - in a real app, you'd want more robust parsing
                param_text = line.replace('PARAMETERS:', '').strip()
                # This is a simplified approach
                
        # For demo purposes, let's handle some basic commands with keyword matching
        command_lower = original_command.lower()
        
        if 'add user' in command_lower or 'create user' in command_lower:
            # Try to extract name and email from command
            words = original_command.split()
            name = None
            email = None
            phone = None
            city = None
            
            # Simple extraction - look for patterns
            for i, word in enumerate(words):
                if word.lower() in ["name", "called", "named"] and i + 1 < len(words):
                    name = words[i + 1]
                elif "@" in word:
                    email = word
                elif word.lower() == "phone" and i + 1 < len(words):
                    phone = words[i + 1]
                elif word.lower() == "city" and i + 1 < len(words):
                    city = words[i + 1]
            
            if name and email:
                user_id = str(uuid.uuid4())
                user = {
                    'id': user_id,
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'city': city,
                    'created_at': datetime.now().isoformat()
                }
                add_user(user)
                return f"✅ User '{name}' added successfully with email {email}, phone {phone or 'N/A'}, and city {city or 'N/A'}!"
            else:
                return "❌ Please provide both name and email. Example: 'Add user named John with email john@example.com phone 123-456-7890 city New York'"
        
        elif 'list users' in command_lower or 'show users' in command_lower:
            users = list_users()
            if users:
                user_list = "\n".join([f"• {user['name']} ({user['email']})" for user in users])
                return f"📋 Current users:\n{user_list}"
            else:
                return "📋 No users found."
        
        elif 'delete user' in command_lower or 'remove user' in command_lower:
            # Extract user name
            words = original_command.split()
            name = None
            for i, word in enumerate(words):
                if word.lower() in ['user', 'named'] and i + 1 < len(words):
                    name = words[i + 1]
                    break
            
            if name:
                user = get_user(name=name)
                if user:
                    delete_user(user['id'])
                    return f"✅ User '{name}' deleted successfully!"
                else:
                    return f"❌ User '{name}' not found."
            else:
                return "❌ Please specify the user name to delete. Example: 'Delete user John'"
        
        elif 'get user' in command_lower or 'find user' in command_lower or 'show user' in command_lower:
            # Extract user name
            words = original_command.split()
            name = None
            for i, word in enumerate(words):
                if word.lower() in ['user', 'named'] and i + 1 < len(words):
                    name = words[i + 1]
                    break
            
            if name:
                user = get_user(name=name)
                if user:
                    return f"👤 User Info:\n• Name: {user['name']}\n• Email: {user['email']}\n• Phone: {user.get('phone', 'N/A')}\n• City: {user.get('city', 'N/A')}\n• Created: {user.get('created_at', 'Unknown')}"
                else:
                    return f"❌ User '{name}' not found."
            else:
                return "❌ Please specify the user name to find. Example: 'Get user John'"
        
        elif 'update user' in command_lower:
            # Extract user name and new data from command
            words = original_command.split()
            name_to_update = None
            new_email = None
            new_phone = None
            new_city = None

            # Simple extraction - look for patterns
            for i, word in enumerate(words):
                if word.lower() == 'user' and i + 1 < len(words):
                    name_to_update = words[i + 1]
                elif word.lower() == 'email' and i + 1 < len(words):
                    new_email = words[i + 1]
                elif word.lower() == 'phone' and i + 1 < len(words):
                    new_phone = words[i + 1]
                elif word.lower() == 'city' and i + 1 < len(words):
                    new_city = words[i + 1]

            if name_to_update:
                user = get_user(name=name_to_update)
                if user:
                    new_data = {}
                    if new_email: new_data['email'] = new_email
                    if new_phone: new_data['phone'] = new_phone
                    if new_city: new_data['city'] = new_city

                    if new_data:
                        result = update_user(user['id'], new_data)
                        if result:
                            return f"✅ User '{name_to_update}' updated successfully!"
                        else:
                            return f"❌ Failed to update user '{name_to_update}'."
                    else:
                        return "❌ Please provide data to update (e.g., email, phone, city)."
                else:
                    return f"❌ User '{name_to_update}' not found."
            else:
                return "❌ Please specify the user name to update. Example: 'Update user John email new@example.com'"
    
        else:
            return """
            🤖 I can help you manage users! Here are some commands you can try:
            
            • **Add user**: "Add user named John with email john@example.com"
            • **List users**: "List all users" or "Show users"
            • **Get user**: "Get user John" or "Find user John"
            • **Update user**: "Update user John email new@example.com phone 123-456-7890 city New York"
            • **Delete user**: "Delete user John" or "Remove user John"
            
            Just type your command naturally!
            """

    except Exception as e:
        return f"❌ Error executing command: {str(e)}"

# Main app
def main():
    st.title("🤖 User Management Chatbot")
    st.markdown("Welcome to the User Management Chatbot! Type natural language commands to manage users.")
    
    # Navigation info
    st.sidebar.markdown("### 📱 Navigation")
    st.sidebar.markdown("- **Chatbot**: This page - interact with the AI assistant")
    st.sidebar.markdown("- **User List**: View all users in a table format")
    
    # Chat interface
    st.subheader("💬 Chat")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Bot:** {message['content']}")
    
    # Input field
    user_input = st.text_input("Type your command here:", key="user_input")
    
    if st.button("Send"):
        if user_input.strip():
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now().isoformat()
            })
            
            # Process command
            with st.spinner("Processing your command..."):
                response = execute_action("", user_input)  # We're using simple keyword matching for now
            
            # Add bot response to history
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': response,
                'timestamp': datetime.now().isoformat()
            })
            
            # Clear input and rerun to show updated chat
            st.rerun()
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

if __name__ == "__main__":
    main()


