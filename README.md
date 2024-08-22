# RAG-ArXiv LLM Research Assistant

## 1. Motivation
The RAG-ArXiv LLM Research Assistant project aims to create an intelligent system that scrapes recent Language Model (LLM) research papers from ArXiv, embeds them, and stores them in a vector database. This setup enables the system to rank and answer LLM-related questions using up-to-date information from the latest research.

### 1.1. Visualization of the RAG app architecture
![Architecture Visualization](https://github.com/user-attachments/assets/9b256c6e-789a-44bc-a585-f6859fc00b41)

## 2. Setup

### 2.1. Prerequisites

Before you begin, ensure you have the following installed on your machine:

#### 2.1.1. Ollama

Set up [Ollama](https://ollama.com/download), a powerful local language model processing tool. Visit their [GitHub](https://github.com/ollama/ollama) to pull the Llama3.1 8B model to your local machine, or follow these steps:

After downloading Ollama, run this command in your terminal:

```bash
ollama pull llama3.1
```

To use a different LLM, select any model from the Ollama website, then navigate to `chat_core/chatbot.py` and change `llm = OllamaLLM(model="llama3.1")` to your preferred model.

#### 2.1.2. Python

Download Python from https://www.python.org/downloads/. Python 3.10 is recommended for this app.

### 2.2. Installation

#### 2.2.1. Clone the repository

Run the following commands in your terminal:

```bash
git clone https://github.com/dohoanggiahuy317/RAG-ArXiv-LLM-Research-Assistant-Proj.git
cd RAG-ArXiv-LLM-Research-Assistant
```

#### 2.2.2. Set up the virtual environment

OPTION 1: If you choose to download the provided virtual environment [here](AAA), activate it using:

```bash
pip install -r requirements.txt
```

OPTION 2: Set up a new virtual environment (you can use conda) with python 3.10, activate it, then install the required packages:

```bash
pip install -r requirements.txt
```

## 3. Start the app

To launch the application, run:

```bash
python app.py
```

The application will be accessible at http://127.0.0.1:5000/ in your browser.

## 4. How to use

The application follows these steps:
1. Fetch data from ArXiv
2. (Optional) Fine-tune your own embedder
3. Save papers into your local vector database
4. Save the model configuration for chatting
5. Create username

(You must complete all 5 steps before you can start chatting)

### 4.0. Use pre-trained fetch data and model

Skip steps 1, 2, and 3 by downloading the prepared data and model:

- [data](AAA): Save this folder into the root directory
- [database](AAA): Save this folder into the root directory
- [models](AAA): Save this folder under the `finetune_embedder` folder
- [data_embedder](AAA): Save this folder under the `finetune_embedder` folder

### 4.1. Step 1 (skip if you completed 4.0)

Fetch new Natural Language Processing papers from ArXiv. Adjust parameters in the window. Already scraped papers will be skipped to avoid duplicates.

### 4.2. Step 2 (skip if you completed 4.0)

Fine-tune your own retrieval model to improve the paper reference engine. Enter your chosen embedder name when prompted.

### 4.3. Step 3 (skip if you completed 4.0)

Save documents to the database using your selected embedder. Choose between the default Hugging Face embedder or any custom embedder you prefer.

### 4.4. Step 4

Save the model configuration for chatting. Select the vector database to query and the compressed document type. LLM Filter is generally more efficient for summarizing long text.

- LLM Extract: Iterates over initially returned documents and extracts only content relevant to the query.
- LLM Filter: A simpler but more robust compressor that uses an LLM chain to filter out irrelevant documents without manipulating their contents.

### 4.5. Step 5

Enter your username to start chatting. Access previous chats by using the same username.

## 5. Checking the references

All responses are referenced based on actual research papers. Citations are shown when the app first provides an answer. You can always find them in `chat_core/logs` using your username, conversation ID, and compression type.

### 5.1. Viewing chat history in the Database

To explore the database contents, use MySQLWorkbench or your preferred SQL tool. Connect to the database file located at `chat_core/database/memory.db` to query and explore the data.

## 6. Contribution

We welcome contributions! If you have suggestions or improvements, please open an issue or submit a pull request on our GitHub repository.