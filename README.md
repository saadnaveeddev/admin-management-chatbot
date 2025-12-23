# admin-management


# User Management Chatbot

A Streamlit-based chatbot application for admins to manage user information using natural language commands. The application uses the Gemini API for understanding commands and stores data in a local JSON file.

## Features

- **Natural Language Interface**: Interact with the chatbot using plain English commands
- **Complete User Management**: Add, view, update, and delete users with full information
- **Extended User Data**: Supports name, email, phone number, and city fields
- **Two-Page Interface**: 
  - Chatbot interface for natural language interactions
  - User list viewer for tabular data display
- **Advanced Search**: Search users by name, email, phone, or city
- **Data Export**: Export user data to CSV format
- **Persistent Storage**: User data stored in JSON format
- **Working Update Function**: Successfully update user information via natural language

## Prerequisites

- Python 3.11 or higher
- Gemini API key (from Google AI Studio)

## Installation

1. **Clone or download the project files**
2. **Navigate to the project directory**:
   ```bash
   cd chatbot_app
   ```

3. **Create and activate virtual environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   - Edit the `.env` file and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key and paste it in the `.env` file

## Running the Application

1. **Activate the virtual environment** (if not already activated):
   ```bash
   source venv/bin/activate
   ```

2. **Start the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** and navigate to `http://localhost:8501`

## Usage

### Chatbot Commands

The chatbot understands natural language commands. Here are some examples:

- **Add a user**: "Add user named John with email john@example.com phone 123-456-7890 city New York"
- **List all users**: "List all users" or "Show users"
- **Find a user**: "Get user John" or "Find user John"
- **Update a user**: "Update user John email new@example.com phone 555-1234 city Boston"
- **Delete a user**: "Delete user John" or "Remove user John"

### User List Viewer

- Navigate to the "User List" page using the sidebar
- View all users in a table format with name, email, phone, city, and creation date
- Search users by any field (name, email, phone, or city)
- Export data to CSV format
- Refresh the list to see latest updates

## File Structure

```
chatbot_app/
├── app.py                    # Main Streamlit application
├── pages/
│   └── 1_User_List.py       # User list viewer page
├── user_manager.py          # User data management functions
├── gemini_integration.py    # Gemini API integration
├── users.json              # User data storage (created automatically)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md              # This file
```

## API Integration

The application integrates with Google's Gemini API for natural language processing. The current implementation uses simple keyword matching for demo purposes, but can be enhanced to use Gemini's full capabilities for more sophisticated command understanding.

## Data Storage

User data is stored in a local `users.json` file with the following structure:

```json
[
  {
    "id": "unique-user-id",
    "name": "User Name",
    "email": "user@example.com",
    "phone": "123-456-7890",
    "city": "City Name",
    "created_at": "2025-06-23T11:26:23.123456"
  }
]
```

## Troubleshooting

### Common Issues

1. **Port already in use**: If port 8501 is busy, use a different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```

2. **Gemini API errors**: Ensure your API key is correctly set in the `.env` file

3. **Module not found**: Make sure you've activated the virtual environment and installed dependencies

### Testing

Run the test script to verify user management functions:
```bash
python test_user_management.py
```

## Development

### Adding New Commands

To add new chatbot commands:

1. Update the `execute_action` function in `app.py`
2. Add keyword matching logic for your new command
3. Implement the corresponding user management function in `user_manager.py`

### Enhancing Gemini Integration

The current implementation uses basic keyword matching. To use Gemini's full capabilities:

1. Update the `process_command` function in `app.py`
2. Enhance the prompt engineering in `gemini_integration.py`
3. Implement structured response parsing
