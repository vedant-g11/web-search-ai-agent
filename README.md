# Streamlit Web Search & Summarization Agent

This project is a web search agent built with Streamlit. It takes a user's query, performs a real-time web search using the SerpAPI, and then leverages a Large Language Model (Google's Gemini 1.5 Flash) to generate a comprehensive, well-structured summary of the search results.

The application is designed with an asynchronous backend to ensure a non-blocking, responsive user experience.



## ✨ Features

-   **Interactive Chat Interface**: A simple and intuitive UI built with Streamlit.
-   **Real-Time Web Search**: Utilizes the SerpAPI to fetch the latest Google search results.
-   **LLM-Powered Summarization**: Employs Google's Gemini 1.5 Flash via LangChain to provide intelligent, structured answers based on the search context.
-   **Asynchronous Pipeline**: Uses `asyncio` to perform API calls without blocking the main application thread, ensuring a smooth UI.
-   **Easy Deployment**: Ready to be deployed on Streamlit Cloud with built-in support for secret management.

## 🛠️ Core Technologies

-   **Framework**: [Streamlit](https://streamlit.io/)
-   **Web Search**: [SerpAPI](https://serpapi.com/)
-   **LLM**: [Google Gemini 1.5 Flash](https://deepmind.google/technologies/gemini/)
-   **Orchestration**: [LangChain](https://www.langchain.com/)

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.8 or higher
-   Git

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
```

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

-   **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
-   **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 3. Install Dependencies

Create a `requirements.txt` file with the following content:

```txt
streamlit
langchain-google-genai
langchain-core
serpapi-python
python-dotenv
```

Then, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

The application requires API keys for both SerpAPI and Google AI.

Create a file named `.env` in the root of your project directory and add your keys:

```ini
# .env file
SERPAPI_API_KEY="your_serpapi_api_key_here"
GOOGLE_API_KEY="your_google_api_key_here"
```

> **Note on Deployment:** If you deploy this to Streamlit Cloud, you should not use a `.env` file. Instead, add your API keys to the Streamlit Cloud secrets manager as described in their [documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management). The code is already configured to read from Streamlit's secrets.

### 5. Run the Application

Once the setup is complete, you can run the Streamlit app with the following command:

```bash
streamlit run main.py
```

Open your web browser and navigate to `http://localhost:8501`.

## ⚙️ How It Works

The application follows a simple, yet powerful, pipeline:

1.  **User Input**: The user enters a query into the Streamlit chat input.
2.  **Web Search**: The `run_pipeline` function is triggered. It makes an asynchronous call to the **SerpAPI** to get the top 5 Google search results related to the query.
3.  **Context Preparation**: The titles, snippets, and links from the search results are formatted into a context block.
4.  **LLM Invocation**: This context, along with the original user prompt, is passed to a **LangChain** pipeline. The pipeline uses a `ChatPromptTemplate` to instruct the Gemini model to act as an expert researcher.
5.  **Summarization**: The **Gemini 1.5 Flash** model processes the information and generates a well-structured, comprehensive answer based *only* on the provided search context.
6.  **Display Response**: The final, formatted response from the model is displayed in the chat interface, and the conversation is saved to the session state.
