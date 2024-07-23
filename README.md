<h1><span style="color: crimson;">gitlit</span> - Assistant 
gitlit is an AI Assistant that was designed to supercharge the development experience with the Python, Langchain, and Streamlit frameworks. It acts as an AI-infused sidekick, offering on-the-fly assistance 🚀, code snippets ✂️, and a deep dive into api code. 🧪

## Dynamic Features:

- Interactive Chat Interface 💬: Engage in a lively chat with gitlit, asking anything from simple how-tos to complex queries. The assistant is equipped to understand and respond with pertinent information, making the interaction both enriching and delightful.

- Code Snippet Wizardry 🧙‍♂️: gitlit conjures up ready-to-use code snippets for common Streamlit scenarios. This magic is especially handy for beginners who are getting to grips with Streamlit and seasoned pros looking to expedite their code-writing spells.

- A Personal Touch 🎨: Decked out with custom CSS and the potential for further personalization, gitlit's UI/UX shines, offering a user experience that's both engaging and aesthetically pleasing.

## Insightful Logic and Capabilities:

At the heart of gitlit lies a sophisticated AI engine 🤖, trained on a plethora of data, including the vast expanses of Streamlit's documentation, forums, and community contributions. This training enables the assistant to understand context, maintain conversational flow, and provide accurate, context-aware advice.

gitlit's backend is a creative use of session state management, providing gitlit with a memory, making for a consistent and coherent conversation for all your coding assistances 🧠.

With Streamlit's caching mechanisms under the hood for performance optimization, and a comprehensive error handling protocol 🛠️, gitlit ensures a smooth sail through the sometimes choppy waters of coding challenges.

gitlit embraces the future with open arms, designed to be extensible and modular. The integration of LangChain adds for a fuller and seamless conversational experience, making it not just an assistant but a developer's companion 🤝.

In the vibrant world of Streamlit development, gitlit shines as a beacon of innovation and practicality. It's not just an AI assistant; it's a testament to the harmonious blend of human creativity and artificial intelligence, all wrapped up in a user-friendly package 🎁. Whether you're a novice coder or a seasoned developer, gitlit is here to light up your coding journey with a spark of AI brilliance ✨.

## Setup Instructions

To get gitlit up and running on your local machine, follow these steps:

### Prerequisites

- Python 3.10 or higher
- Pip package manager

### API Keys

Use secrets.toml an add your OpenAI API key or set your enviroment variable OPENAI_API_KEY to your API key.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/mearnsb/gitlit.git
cd gitlit
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

### Running the Application

To run gitlit, execute the following command:

```bash
streamlit run gitlit.py
```

This will start the Streamlit server, and you should see output indicating the local URL where the app is being served, typically `http://localhost:8501`.

## Using gitlit

After launching gitlit, you can interact with it in the following ways:

- **Chat Interface**: Simply type your Streamlit-related queries into the chat interface and hit send. gitlit will respond with insights, code snippets, or guidance based on your questions.

- **Code Examples**: Ask for code examples by typing queries such as "How do I create a sidebar in Streamlit?" and gitlit will provide you with the relevant code.

Remember to check the sidebar for additional features and settings that you can customize according to your needs.

## Contributions

If you'd like to contribute to gitlit, please fork the repository and create a pull request with your features or fixes.

## License

gitlit is released under the [MIT License](LICENSE). See the `LICENSE` file for more details.
