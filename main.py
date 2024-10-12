import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq
import time

def parse_groq_stream(stream):
    """Parse the streaming response from the Groq API."""
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

# Streamlit page configuration
st.set_page_config(
    page_title="Field Focus",
    page_icon="🤖",
    layout="centered",
)

# Load environment variables
try:
    secrets = dotenv_values(".env")  # For development environment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except KeyError:
    secrets = st.secrets  # For Streamlit deployment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

# Save the API key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Set default values if keys are missing
INITIAL_RESPONSE = secrets.get("INITIAL_RESPONSE", "Hello! How can I assist you today?")
INITIAL_MSG = secrets.get("INITIAL_MSG", "Welcome to Field Focus!")
CHAT_CONTEXT = secrets.get("CHAT_CONTEXT", "You are a helpful assistant knowledgeable about sports gear and equipment.")

client = Groq()

# Initialize the chat history if not present in Streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE},
    ]

# Page title
st.title("Welcome to Field Focus! 🤓")
st.caption("Your Personal Assistant for All Things Sports Gear!")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar='🤖' if message["role"] == "assistant" else "🗨️"):
        st.markdown(message["content"])

# User input field
user_prompt = st.chat_input("Ask me")

if user_prompt:
    # Display user message
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    
    # Append user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Prepare messages for the Groq API
    messages = [
        {"role": "system", "content": CHAT_CONTEXT},
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar='🤖'):
        # Show "Thinking..." message with loading spinner
        with st.spinner("Thinking..."):
            time.sleep(2)  # Simulate thinking time

            # Now get the actual response from the Groq API
            try:
                stream = client.chat.completions.create(
                    model="gemma-7b-it",
                    messages=messages,
                    stream=True  # For streaming the message
                )

                # Get the full response from the stream
                full_response = ''.join(parse_groq_stream(stream))

                # Display the actual response
                st.markdown(full_response)

                # Append assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"Error: {e}")

    # Scroll to the bottom of the chat by displaying an empty message
    st.write("")  # To push content down, allowing for scrolling
