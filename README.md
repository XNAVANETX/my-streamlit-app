# Chatbot-Streamlit 🤖

Welcome to **Chatbot-Streamlit**! This project features a user-friendly AI chatbot application built with Streamlit, designed to provide instant support and information through an interactive chat interface.

## 🌟 Features

- **Interactive Chat Interface**: 
  - Engage in real-time conversations with the chatbot for immediate responses.
  
- **Contextual Understanding**: 
  - The chatbot is equipped to comprehend and efficiently respond to a variety of inquiries.
  
- **Customizable**: 
  - Easily modify the underlying code to tailor the chatbot’s responses and functionalities according to your needs.

## ⚙️ Installation

### Prerequisites

Before you begin, ensure that you have Python **3.7** or higher installed on your machine. You can check your Python version by running:

```bash
python --version
```

### Clone the Repository

Clone this repository to your local machine by executing:

```bash
git clone https://github.com/Divith123/Chatbot-Streamlit.git
cd Chatbot-Streamlit
```

### Setup Environment

1. **Create a Virtual Environment (Optional but Recommended)**:
   - It's a good practice to use a virtual environment to manage your project's dependencies. Create one using:

   ```bash
   python -m venv venv
   ```

   - Activate the virtual environment:

     ```bash
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

2. **Install Required Dependencies**:
   - Install the necessary libraries specified in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` File**:
   - In the project directory, create a `.env` file for any necessary configurations (e.g., API keys):

   ```plaintext
   GROQ_API_KEY=your_api_key
   ```
**Change this to your need**:
    INITIAL_RESPONSE="Hello! How can I assist you today?"
    INITIAL_MSG="Welcome to Field Focus!"
    CHAT_CONTEXT="You are a helpful assistant knowledgeable about sports gear and equipment."
    
## 🚀 Running the Chatbot

To launch the application, run the following command:

```bash
streamlit run main.py
```

This will open the application in your default web browser.

## 📄 Code Overview

Below is a brief overview of the main code structure in `main.py`:

```python
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
```

## 🤝 Contributing

Contributions are more than welcome! If you have ideas for enhancements or new features, please feel free to fork the repository and submit a pull request.

## 📄 License

This project is licensed under the MIT License. For more details, please refer to the [LICENSE](LICENSE) file.

## 📫 Contact

For any questions or inquiries, feel free to reach out:

- **Email**: [ninja@ninjaonsteroids.me](mailto:ninja@ninjaonsteroids.me)
- **GitHub**: [Divith123](https://github.com/Divith123)
