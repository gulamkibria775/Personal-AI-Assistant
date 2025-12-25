import streamlit as st
from config.settings import Settings
from jarvis.gemini_engine import GeminiEngine
from jarvis.prompt_controller import PromptController
from jarvis.memory import Memory
from jarvis.assistant import JarvisAssistant

st.set_page_config("JARVIS AI", "🤖", layout="wide")
st.title(" Personal AI Assistant")

# ---------------- Session State ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "memory" not in st.session_state:
    st.session_state.memory = None

# ---------------- Sidebar ----------------
with st.sidebar:
    if not st.session_state.logged_in:
        page = st.radio("Menu", ["Login", "Register"])
    else:
        st.success(f"Welcome {st.session_state.user}")

        if st.button("Clear Memory"):
            st.session_state.memory.clear()
            st.success("Memory Cleared")

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.memory = None
            st.rerun()

# ---------------- Auth ----------------
if not st.session_state.logged_in:

    if page == "Register":
        name = st.text_input("Name")
        email = st.text_input("Email",placeholder="example@gmail.com")
        pwd = st.text_input("Password", type="password")

        if st.button("Register"):
            if name.strip() == "" or email.strip() == "" or pwd.strip() == "":
                st.error("All fields are required!")
            else:
                st.session_state.users[email] = {
                "name": name,
                "password": pwd
            }
                st.success("Registered Successfully")


    if page == "Login":
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if email in st.session_state.users and st.session_state.users[email]["password"] == pwd:
                st.session_state.logged_in = True
                st.session_state.user = st.session_state.users[email]["name"]
                st.session_state.memory = Memory(
                    filename=f"memory_{email.replace('@','_')}.json"
                )
                st.rerun()
            else:
                st.error("Invalid Credentials")

# ---------------- NLP ----------------
else:
    # Initialize core components
    settings = Settings()
    api_key = settings.load_api_key()

    if not api_key:
        st.error("API key not found. Please configure your API key.")
        st.stop()

    engine = GeminiEngine(api_key)
    prompt_controller = PromptController()
    assistant = JarvisAssistant(
        engine,
        prompt_controller,
        st.session_state.memory
    )

    # Feature selection
    feature = st.selectbox(
        "Select NLP Feature",
        ["Select feature", "Sentiment Analysis", "Language Translation", "Language Detection"]
    )

    text = st.text_area("Enter text", placeholder="Type your text here...")

    if st.button("Run"):
        if feature == "Select feature":
            st.error(" Please select an NLP feature")
        elif not text.strip():
            st.error("Text input cannot be empty")
        else:
            task_map = {
                "Sentiment Analysis": "sentiment",
                "Language Translation": "translation",
                "Language Detection": "detection"
            }

            # Store user message
            st.session_state.memory.add("user", text)

            # Run task
            result = assistant.run_task(task_map[feature], text)

            # Store assistant response
            st.session_state.memory.add("assistant", result)

            st.subheader("Result")
            st.write(result)

    # Conversation history
    st.divider()
    st.subheader("Conversation History")

    for msg in st.session_state.memory.get_history():
        role = "User" if msg["role"] == "user" else "JARVIS"
        st.markdown(f"**{role}:** {msg['message']}")
