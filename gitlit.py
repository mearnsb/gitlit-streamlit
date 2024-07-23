import logging
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from langchain.adapters import openai as lc_openai
#from PIL import Image, ImageEnhance (removed #Image from requirements.txt)
import time
import json
import requests
import base64
import dg #data generator
from faker import Faker
import uuid 

from openai import OpenAI, OpenAIError
client = OpenAI()

logging.basicConfig(level=logging.INFO)

# Page Configuration
st.set_page_config(
    page_title="gitlit - An Intelligent Assistant",
    page_icon="imgs/avatar_streamly.png",
    layout="wide",
    #initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/mearnsb/gitlit",
        "Report a bug": "https://github.com/mearnsb/gitlit",
        "About": """
            ## gitlit
            
            **GitHub**: https://github.com/brianmearns/
            
            The AI Assistant named, gitlit, aims to provide helpful answers and resopnses.,
            generate code snippets
            and answer questions, and more.
        """
    }
)

st.title("gitlit")

API_DOCS_URL = "https://docs.streamlit.io/library/api-reference"

@st.cache_data(show_spinner=False)
def long_running_task(duration):
    """
    Simulates a long-running operation.
    """
    time.sleep(duration)
    return "Long-running operation completed."

@st.cache_data(show_spinner=False)
def load_updates():
    """Load the latest updates from a local JSON file."""
    try:
        with open("data/streamlit_updates.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@st.cache_data(show_spinner=False)
def get_latest_update_from_json(keyword, latest_updates):
    """
    Fetch the latest updates based on a keyword.

    Parameters:
        keyword (str): The keyword to search for in the updates.
        latest_updates (dict): The latest updates data.

    Returns:
        str: The latest update related to the keyword, or a message if no update is found.
    """
    for section in ["Highlights", "Notable Changes", "Other Changes"]:
        for sub_key, sub_value in latest_updates.get(section, {}).items():
            for key, value in sub_value.items():
                if keyword.lower() in key.lower() or keyword.lower() in value.lower():
                    return f"Section: {section}\nSub-Category: {sub_key}\n{key}: {value}"

    return "No updates found for the specified keyword."

def get_api_code_version():
    """
    Get the current API code version from the API documentation.

    Returns:
        str: The current API code version.
    """
    try:
        response = requests.get(API_DOCS_URL)
        if response.status_code == 200:
            return "1.34.0"
    except requests.exceptions.RequestException as e:
        print("Error connecting to the  API documentation:", str(e))
    return None

def display_updates():
    """It displays the latest updates."""
    with st.expander("1.34 Information", expanded=False): st.markdown("For more details on this version, check out the [Forum post](https://docs.streamlit.io/library/changelog#version).")

@st.cache_data(show_spinner=False)
def on_chat_submit(chat_input, api_key, latest_updates, use_langchain=False):
    """
    Handle chat input submissions and interact with the OpenAI API.

    Parameters:
        chat_input (str): The chat input from the user.
        api_key (str): The OpenAI API key.
        latest_updates (dict): The latest updates fetched from a JSON file or API.
        use_langchain (bool): Whether to use LangChain OpenAI wrapper.

    Returns:
        None: Updates the chat history in session state.
    """
    user_input = chat_input.strip().lower()

    # Initialize the OpenAI API
    model_engine = "gpt-3.5-turbo-0125"

    # Initialize the conversation history with system and assistant messages
    if 'conversation_history' not in st.session_state:
        assistant_message = "Hello, I'm here to help. I am gitlit. How can I assist you today?"
        formatted_message = []
        highlights = latest_updates.get("Highlights", {})
        
        # Include version info in highlights if available
        version_info = highlights.get("Version 1.34", {})
        if version_info:
            description = version_info.get("Description", "No description available.")
            formatted_message.append(f"- **Version 1.34**: {description}")

        for category, updates in latest_updates.items():
            formatted_message.append(f"**{category}**:")
            for sub_key, sub_values in updates.items():
                if sub_key != "Version 1.34":  # Skip the version info as it's already included
                    description = sub_values.get("Description", "No description available.")
                    documentation = sub_values.get("Documentation", "No documentation available.")
                    formatted_message.append(f"- **{sub_key}**: {description}")
                    formatted_message.append(f"  - **Documentation**: {documentation}")

        assistant_message += "\n".join(formatted_message)
        
        # Initialize conversation_history
        st.session_state.conversation_history = [
            {"role": "system", "content": "You are gitlit, a specialized AI assistant trained in python."},
            {"role": "system", "content": "Refer to conversation history to provide context to your reponse."},
            {"role": "assistant", "content": assistant_message}
        ]

    # Append user's query to conversation history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    try:
        # Logic for assistant's reply
        assistant_reply = ""

        if use_langchain:
            # LangChain OpenAI wrapper call
            lc_result = lc_openai.ChatCompletion.create(
                messages=st.session_state.conversation_history,
                model=model_engine,
                temperature=0
            )
            assistant_reply = lc_result["choices"][0]["message"]["content"]

        else:
            if "latest updates" in user_input:
                assistant_reply = "Here are the latest highlights:\n"
                highlights = latest_updates.get("Highlights", {})
                if highlights:
                    for version, info in highlights.items():
                        description = info.get("Description", "No description available.")
                        assistant_reply += f"- **{version}**: {description}\n"
            else:
                
                # Direct OpenAI API call
                response = client.chat.completions.create(model=model_engine,
                messages=st.session_state.conversation_history)
                
                assistant_reply = response.choices[0].message.content

            # Append assistant's reply to the conversation history
            st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})

        # Update the chat history
        if "history" in st.session_state:
            st.session_state.history.append({"role": "user", "content": user_input})
            st.session_state.history.append({"role": "assistant", "content": assistant_reply})

    except OpenAIError.APIConnectionError as e:
        logging.error(f"Error occurred: {e}")
        error_message = f"OpenAI Error: {str(e)}"
        st.error(error_message)
        #st.session_state.history.append({"role": "assistant", "content": error_message})

def main():
    """
    Display and handle the chat interface.
    """
    # Initialize session state variables for chat history and conversation history
    if "history" not in st.session_state:
        st.session_state.history = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if "elements" not in st.session_state:
        st.session_state.elements = []
        
    if "openai_api_key" not in st.session_state:
            st.session_state["openai_api_key"] = ""
        
    # Initialize the chat with a greeting and updates if the history is empty
    if not st.session_state.history:
        latest_updates = load_updates()  # This function should be defined elsewhere to load updates
        initial_bot_message = "Hello! How can I assist you today? Here are some of the latest highlights:\n"
        updates = latest_updates.get("Highlights", {})
        if isinstance(updates, dict):  # Check if updates is a dictionary
            initial_bot_message = "Hello, I'm here to help. I am gitlit. How can I assist you today?"
            st.session_state.history.append({"role": "assistant", "content": initial_bot_message})
            st.session_state.conversation_history = [
                {"role": "system", "content": "You are gitlit, a specialized AI assistant trained to assist with the logic and programming like python and sql."},
                {"role": "system", "content": "Refer to conversation history to provide context to your reponse."},
                {"role": "system", "content": "Use the streamlit_updates.json local file to look up the latest feature updates."},
                {"role": "system", "content": "When responding, provide code examples, links to documentation, and code examples from the API to help the user."},
                {"role": "assistant", "content": initial_bot_message}
            ]
        else:
            st.error("Unexpected structure for 'Highlights' in latest updates.")

    # Sidebar 
    #mode = st.sidebar.radio("Mode:", options=["chat", "duck", "upload", "dataframe"], index=3)
    mode = st.sidebar.radio("Mode:", options=["chat", "data"], index=1)
    use_langchain = False
    st.sidebar.markdown("---")
    
    # Modes
    if mode == "chat":
            
        # Access API Key from st.secrets
        #api_key = st.secrets["OPENAI_API_KEY"]
        api_key = st.sidebar.text_input(
        label="OpenAI API Key",
        type="password",
        )

        st.session_state['openai_api_key'] = api_key
        
        if not api_key and not len(st.session_state['openai_api_key']) < 1:
            st.error("Please add your OpenAI API key")
            st.stop()

        chat_input = st.chat_input("Ask me for assistance:")
        if chat_input:
            latest_updates = load_updates()
            on_chat_submit(chat_input, api_key, latest_updates, use_langchain)

        # Display chat history with custom avatars
        for message in st.session_state.history[-20:]:
            role = message["role"]
            
            # Set avatar based on role
            if role == "assistant":
                avatar_image = "imgs/avatar_streamly.png"
            elif role == "user":
                avatar_image = "imgs/stuser.png"
            else:
                avatar_image = None  # Default
            
            with st.chat_message(role, avatar=avatar_image):
                st.write(message["content"])

    elif mode=="data":
        
        def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
            """
            Adds a UI on top of a dataframe to let viewers filter columns
        
            Args:
                df (pd.DataFrame): Original dataframe
        
            Returns:
                pd.DataFrame: Filtered dataframe
            """
            #modify = st.checkbox("Filters", value=True)
            modify=True
            if not modify:
                return df
        
            df = df.copy()
            
            modification_container = st.container()
        
            with modification_container:
                to_filter_columns = st.multiselect("Columns to filter", df.columns, default="id")
                for column in to_filter_columns:
                    left, right = st.columns((1, 20))
                    user_text_input = st.text_input(
                        f"Search {column} column (regex capable filter)"
                    )
                    if user_text_input:
                        df = df[df[column].astype(str).str.contains(user_text_input)]
        
            return df
        
        df = pd.read_csv('data/faker_name_list.csv')
        df = df[['id','example','description']]
        df = df[~df["id"].str.startswith("_")]
        df.insert(0, 'is_selected', False) # df['is_selected'] = False
        fdf = filter_dataframe(df)

        def update_value():
            """
            Located on top of the data editor.
            """
            st.session_state["editor_key"] = str(uuid.uuid4())

        # session state 
        if "editor_key" not in st.session_state:
            st.session_state["editor_key"] = str(uuid.uuid4())
                    
        if "df_value" not in st.session_state:
            st.session_state["df_value"] = fdf

        # Reset
        reset_button = st.button("Reset", on_click=update_value)
        if reset_button:
            st.session_state['elements'] = []

        # Columns
        left, right = st.columns(2)
        with left:
            st.subheader("Available data elements")
            
            def update(edited_df):
                for item_1, item_2, item_3, item_4 in zip(
                    edited_df["id"], edited_df["example"], edited_df["description"], edited_df['is_selected']
                ):
                    if item_4 == True:
                        #st.write((item_1, item_2, item_3, item_4))
                        if item_1 not in st.session_state['elements']:
                            st.session_state['elements'].append(item_1)
            
            edited_df = st.data_editor(
                fdf,
                key=st.session_state["editor_key"],
                num_rows="dynamic",
            )
            
            if edited_df is not None and not edited_df.equals(st.session_state["df_value"]):
                update(edited_df)
                st.session_state["df_value"] = edited_df
            
        with right:
            st.subheader("Selected data elements")
            st.write(st.session_state['elements'])
            
        st.subheader("Snippet")
        code_logic = dg.fuzz_generate_string(st.session_state['elements'])
        template = f'''import pandas as pd
from faker import Faker
f = Faker()
items = []
for _ in range(10):

    {code_logic}
    items.append(data)

row_num = [i for i in range(0, len(items))]
example = pd.DataFrame(items, index=row_num).rename_axis('_row_num')

print(example.head())'''.replace('Faker().', 'f.')

        st.code(template)

        st.subheader("Download")
        try:
            from io import StringIO
            from contextlib import redirect_stdout
            def run_code(code):
              f = StringIO()
              with redirect_stdout(f):
                exec(code)
                s = f.getvalue()
              return s
            output = run_code(template)
            
            o = run_code(template.replace("print(example.head())", "st.write(example)"))
            st.code(output)
            
        except Exception as e:
            st.error(e)

    else:
        display_updates()
        

if __name__ == "__main__":
    main()
