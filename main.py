import streamlit as st
import requests
from groq import Groq
import time
import json
from datetime import datetime
import pickle
import os

# Page config for a cleaner look
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling - keeping the previous UI
st.markdown("""
    <style>
    .chat-sidebar {
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .chat-button {
        width: 100%;
        margin: 0.2rem 0;
        text-align: left;
        padding: 0.5rem;
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        cursor: pointer;
    }
    .chat-button:hover {
        background-color: #e9ecef;
    }
    .chat-button.active {
        background-color: #e6f3ff;
        border-color: #0d6efd;
    }
    .chat-container {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        height: calc(100vh - 200px);
        overflow-y: auto;
    }
    .user-message {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .assistant-message {
        background-color: #e6f3ff;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 80%;
    }
    .message-timestamp {
        font-size: 0.8em;
        color: #6c757d;
        margin-top: 5px;
    }
    .new-chat-btn {
        background-color: #0d6efd;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        text-align: center;
        cursor: pointer;
    }
    .delete-chat-btn {
        color: #dc3545;
        float: right;
        cursor: pointer;
    }
    .stTextInput {
        position: fixed;
        bottom: 20px;
        left: 33%;
        right: 2%;
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


# Initialize storage
def ensure_storage_directory():
    """Ensure the storage directory exists"""
    os.makedirs('.streamlit', exist_ok=True)


def save_chats_to_storage():
    """Save chats to local storage"""
    ensure_storage_directory()
    try:
        with open('.streamlit/chat_storage.pkl', 'wb') as f:
            pickle.dump(st.session_state.chats, f)
    except Exception as e:
        st.warning(f"Failed to save chats: {str(e)}")


def load_chats_from_storage():
    """Load chats from local storage"""
    try:
        with open('.streamlit/chat_storage.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return {}


# Initialize session state
if 'chats' not in st.session_state:
    st.session_state.chats = load_chats_from_storage()
if 'current_chat_id' not in st.session_state:
    st.session_state.current_chat_id = None
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""


def search_wikipedia(prompt):
    """Search Wikipedia for the given prompt."""
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "search": prompt,
    }
    try:
        response = session.get(url=url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('query', {}).get('search', [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error searching Wikipedia: {str(e)}")
        return []


def get_plain_text_extract(page_id):
    """Retrieve plain text extract from Wikipedia."""
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "pageids": page_id,
        "prop": "extracts",
        "explaintext": True,
        "exintro": True,
    }
    try:
        response = session.get(url=url, params=params)
        response.raise_for_status()
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        page = pages.get(str(page_id), {})
        return page.get('extract', '')
    except requests.exceptions.RequestException as e:
        st.error(f"Error retrieving Wikipedia content: {str(e)}")
        return ''


def generate_answer(context, topic):
    """Generate answer using Groq API."""
    try:
        client = Groq()

        if context.strip():
            user_message = f"Summarize the following Wikipedia content for the topic '{topic}':\n\n{context}"
        else:
            user_message = f"No Wikipedia results were found for the topic '{topic}'. Please provide an informative answer on this topic."

        messages = [
            {
                "role": "system",
                "content": "You are a knowledgeable AI assistant. Provide clear, concise, and accurate information."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_completion_tokens=31200,
            top_p=1,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating answer: {str(e)}")
        return "I apologize, but I encountered an error while generating the answer. Please try again."


def process_query(query):
    """Process the user query and generate response."""
    results = search_wikipedia(query)

    if results:
        first_result = results[0]
        page_id = first_result.get('pageid')
        extract_text = get_plain_text_extract(page_id)
    else:
        extract_text = ""

    return generate_answer(extract_text, query)


def create_new_chat():
    """Create a new chat and manage chat limit"""
    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Check if we have 5 or more chats
    if len(st.session_state.chats) >= 5:
        # Remove the oldest chat
        oldest_chat_id = min(st.session_state.chats.keys())
        del st.session_state.chats[oldest_chat_id]

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }
    st.session_state.current_chat_id = chat_id
    save_chats_to_storage()


def delete_chat(chat_id):
    """Delete a specific chat"""
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]
        if st.session_state.current_chat_id == chat_id:
            st.session_state.current_chat_id = next(iter(st.session_state.chats)) if st.session_state.chats else None
        save_chats_to_storage()


def handle_input():
    """Handle user input and generate response"""
    if st.session_state.user_input and st.session_state.current_chat_id:
        query = st.session_state.user_input
        current_chat = st.session_state.chats[st.session_state.current_chat_id]

        # Add user message
        current_chat["messages"].append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now().strftime("%H:%M")
        })

        # Update chat title if it's the first message
        if current_chat["title"] == "New Chat":
            current_chat["title"] = query[:30] + "..." if len(query) > 30 else query

        st.session_state.user_input = ""

        # Generate and add assistant response
        with st.spinner("Searching knowledge base..."):
            response = process_query(query)

        current_chat["messages"].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().strftime("%H:%M")
        })

        save_chats_to_storage()


def main():
    # Render sidebar
    with st.sidebar:
        if st.button("+ New Chat", type="primary"):
            create_new_chat()

        st.markdown("### Your Chats")

        for chat_id, chat_data in st.session_state.chats.items():
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(
                        chat_data["title"],
                        key=f"chat_{chat_id}",
                        use_container_width=True
                ):
                    st.session_state.current_chat_id = chat_id
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    delete_chat(chat_id)

    # Create initial chat if none exists
    if not st.session_state.chats:
        create_new_chat()

    # Main chat area
    if st.session_state.current_chat_id:
        current_chat = st.session_state.chats[st.session_state.current_chat_id]

        st.title(current_chat["title"])

        # Chat messages container
        chat_container = st.container()
        with chat_container:
            for message in current_chat["messages"]:
                if message["role"] == "user":
                    st.markdown(f"""
                        <div class="user-message">
                            {message["content"]}
                            <div class="message-timestamp">{message["timestamp"]}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="assistant-message">
                            {message["content"]}
                            <div class="message-timestamp">{message["timestamp"]}</div>
                        </div>
                    """, unsafe_allow_html=True)

        # Input area
        st.text_input(
            "Ask a question...",
            key="user_input",
            placeholder="Type your question here and press Enter",
            on_change=handle_input
        )


if __name__ == "__main__":
    main()