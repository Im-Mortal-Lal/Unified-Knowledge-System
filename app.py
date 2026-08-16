import streamlit as st
import warnings
import uuid

warnings.filterwarnings("ignore")

from ingest import load_vectorstore
from retriever import retrieve_context
from generator import generate_answer

from database.chat_repository import (
    save_message,
    load_messages,
    delete_chat,
    get_all_sessions,
    get_chat_title
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Machine Manual Chatbot",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# SESSION INITIALIZATION
# --------------------------------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:

    rows = load_messages(
        st.session_state.session_id
    )

    st.session_state.messages = [
        {
            "role": row.Role.lower(),
            "content": row.Message
        }
        for row in rows
    ]


# --------------------------------------------------
# LOAD VECTOR DATABASE
# --------------------------------------------------

@st.cache_resource
def initialize():
    return load_vectorstore()


with st.spinner("Loading machine manuals..."):
    vectorstore = initialize()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("Machine Manual Chatbot")

    # -------------------------------
    # NEW CHAT
    # -------------------------------

    if st.button(
        "🆕 New Chat",
        use_container_width=True
    ):

        st.session_state.session_id = str(uuid.uuid4())

        st.session_state.messages = []

        st.rerun()


    # -------------------------------
    # CLEAR CURRENT CHAT
    # -------------------------------

    if st.button(
        "🗑️ Clear Current Chat",
        use_container_width=True
    ):

        delete_chat(
            st.session_state.session_id
        )

        st.session_state.messages = []

        st.rerun()


    st.divider()


    # -------------------------------
    # PREVIOUS CONVERSATIONS
    # -------------------------------

    st.subheader("Chat History")

    sessions = get_all_sessions()

    for session in sessions:

        title = session.Title

        if not title:
            title = "New Chat"

        title = title[:40]

        if st.button(
            title,
            key=f"session_{session.SessionId}",
            use_container_width=True
        ):

            # Switch session
            st.session_state.session_id = session.SessionId

            # Load messages from SQL Server
            rows = load_messages(
                session.SessionId
            )

            # Put messages into Streamlit session state
            st.session_state.messages = [
                {
                    "role": row.Role.lower(),
                    "content": row.Message
                }
                for row in rows
            ]

            st.rerun()


# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

st.title("Machine Manual Chatbot")

st.caption(
    "Ask questions about the technical manuals loaded into the system."
)


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

query = st.chat_input(
    "Ask a question about the machine manuals..."
)


# --------------------------------------------------
# PROCESS QUESTION
# --------------------------------------------------

if query:

    # ----------------------------------------------
    # DISPLAY USER MESSAGE
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    save_message(
        st.session_state.session_id,
        "user",
        query
    )

    with st.chat_message("user"):
        st.markdown(query)


    # ----------------------------------------------
    # GENERATE ANSWER
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Searching technical manuals..."):

            context, retrieved_docs = retrieve_context(
                vectorstore,
                query
            )

            answer = generate_answer(
                context,
                query
            )

        # Display answer
        st.markdown(answer)

        # ------------------------------------------
        # SHOW PDF IMAGES
        # ------------------------------------------

        


    # ----------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    save_message(
        st.session_state.session_id,
        "assistant",
        answer
    )