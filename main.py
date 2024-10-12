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
    page_title="Nike AI",
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
INITIAL_MSG = secrets.get("INITIAL_MSG", "Welcome to the Nike AI Chatbot!")
CHAT_CONTEXT = secrets.get("CHAT_CONTEXT", "You are a helpful assistant knowledgeable about Nike products and services.")

client = Groq()

# Initialize the chat history if not present in Streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": INITIAL_RESPONSE},
    ]

# Page title
st.title("Welcome to the Nike AI Chatbot! 🤓")
st.caption("Your Personal Assistant for All Things Nike!")

# Detailed introduction
st.markdown("""
**Hello! I'm your Nike AI Assistant, here to help you with:**  

1. **Product Information:** Get details on the latest Nike shoes, apparel, and accessories.
2. **Size Guides:** Need help finding the right fit? I can provide size charts and recommendations.
3. **Product Availability:** Check if your favorite items are in stock at local stores or online.
4. **Ordering Help:** Have questions about placing an order or tracking your shipment? I can assist you!
5. **Nike News:** Stay updated on the latest releases, promotions, and events from Nike.
6. **Customer Support:** I can guide you through common issues or direct you to the right resources.
7. **Personalized Recommendations:** Share your preferences, and I'll suggest products just for you!

**Feel free to ask me anything, and let’s elevate your Nike experience together!**  
""")

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
