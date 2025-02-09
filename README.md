# KnowledgeKeeper

![AI Knowledge Assistant](banner.png)


The **KnowledgeKeeper** is a Streamlit-based chat application that integrates with the Wikipedia and Groq APIs to provide users with concise, informative answers on any topic. The application searches Wikipedia for relevant articles, extracts only the introductory content, and then uses the Groq API to generate a summary or informative answer. If no Wikipedia results are found, the assistant generates an answer directly using Groq.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Interactive Chat Interface**: Communicate with the AI assistant through a modern chat UI.
- **Session Management**: Create, view, and delete up to 5 chat sessions stored locally.
- **Wikipedia Integration**: Search for topics on Wikipedia and extract only the introductory text of the first result.
- **Groq API Summarization**: Use the Groq API to generate clear, concise, and informative answers.
- **Local Storage**: Chat history is saved locally using Python's `pickle` module.
- **Custom Styling**: Enjoy a clean and modern user interface with custom CSS.

---

## Requirements

- **Python 3.7+** (Python 3.8+ is recommended)
- **Streamlit**
- **Requests**
- **Groq** (Python library for accessing the Groq API)
- **Pickle** (standard Python library)
- Other standard libraries: `os`, `datetime`, `time`, `json`

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/achuajays/KnowledgeKeeper.git
   cd KnowledgeKeeper
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install streamlit requests groq 
   ```


---

## Configuration

- **Groq API Key**:  
  Make sure you have access to the Groq API and that your API key is properly configured. You might need to set an environment variable or adjust the Groq client initialization in the code.

- **Local Storage**:  
  Chat sessions are stored locally in a hidden directory (`.streamlit`) using a pickle file (`chat_storage.pkl`). This file is automatically created and managed by the app.

---

## Usage

1. **Run the Application**

   In the terminal, run:
   
   ```bash
   streamlit run main.py
   ```

2. **Chat Interface**

   - **New Chat**: Click the "+ New Chat" button in the sidebar to create a new chat session.
   - **Sending a Query**: Type your question or topic in the text input at the bottom of the screen and press Enter.
   - **Processing**:  
     - The assistant searches Wikipedia for your topic.
     - If a result is found, it extracts the introduction and sends it along with your topic to the Groq API for summarization.
     - If no Wikipedia result is found, it generates an answer directly from Groq.
   - **Viewing the Response**: The conversation history is displayed in the main chat area.

3. **Managing Chat Sessions**

   - **Switch Chats**: All active chats are listed in the sidebar. Click on a chat to load its conversation.
   - **Delete Chat**: Click the trash icon (🗑️) next to a chat to delete that session.
   - **Session Limit**: The app maintains a maximum of 5 chat sessions. When creating a new session beyond this limit, the oldest session is automatically removed.

---

## File Structure

- `main.py`:  
  The main Streamlit application file that contains all the code for the chat interface, Wikipedia search, Groq API integration, and session management.

- `.streamlit/chat_storage.pkl`:  
  A pickle file (created automatically) that stores the chat sessions locally.

---

## Troubleshooting

- **RuntimeError: dictionary changed size during iteration**  
  If you encounter this error, ensure that the code iterates over a static copy of the dictionary using `list(st.session_state.chats.items())`.

- **API Errors**  
  If you experience connectivity or authentication issues with the Groq or Wikipedia API, verify that your internet connection is stable and your API keys/configurations are correct.

- **Dependency Issues**  
  Ensure all required packages are installed.

---

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and open a pull request. For any issues or feature requests, please open an issue on GitHub.

---



## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page)
- [Groq API](https://www.groq.com/)
- Thanks to the open-source community for the invaluable resources and libraries used in this project.

