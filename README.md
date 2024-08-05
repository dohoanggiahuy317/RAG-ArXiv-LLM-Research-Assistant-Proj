# RAG-ArXiv LLM Research Assistant

## Motivation
The ArXiv LLM Research Assistant project aims to create an intelligent system capable of scraping recent research papers on Language Models (LLMs) from ArXiv, embedding the papers, and storing them in a vector database. This setup allows the system to rank and answer any LLM-related questions using up-to-date information from the latest research.

<img width="1062" alt="viz" src="https://github.com/user-attachments/assets/9b256c6e-789a-44bc-a585-f6859fc00b41">


## Setup

### Prerequisites
Before you begin, ensure you have the following installed on your machine:

- [Ollama](https://ollama.com/download): A powerful language model processing tool.
- Python and pip: You can download `Python` from [here](https://www.python.org/downloads/) and install `pip` by following the instructions [here](https://pip.pypa.io/en/stable/installation/).

### Installation
1. Clone the repository:
   
   ```bash
   git clone [https://github.com/yourusername/RAG-LangChain-supreme-bot.git](https://github.com/dohoanggiahuy317/RAG-ArXiv-LLM-Research-Assistant-Proj.git
   cd RAG-ArXiv-LLM-Research-Assistant
   ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```
3. Download and install Ollama:

Follow the instructions here to download and install Ollama on your machine. ## 
 
## Instructions  
   
1. To parse the data, run the following script:


    ```bash
    sh parse_data/command/parse_data.sh
    ``` 

2. To embed the parsed data and save the documents, run:

    ```bash
    sh rag_core/command/save_docs.sh
    ```
    
3. To interact with the bot and ask questions, use:

    ```bash
    sh chat_core/command/chat_core.sh
    ```


## Customizing Parameters

You can change the parameters in `chat_core.sh` to adjust the number of user and question threads. Open `chat_core.sh` in a text editor and modify the following lines:

```bash
# chane user id to have different chat memory
user_id=2

# create new conversation
conversation_id=5
```

To get different papers on various topics, update the `search_query` parameter `in parse_data/command/parse_data.sh`, please refer to ArXiv API for further information:


```bash
# Update this line with your desired search query
search_query="your_custom_search_query"
```

Adjust the numbers according to your requirements.


### Viewing chat history the Database

To view the contents of the database, you can use an MySQLWorkbench application. Open your preferred SQL tool and connect it to the database file located at `chat_core/database/memory.db`. This will allow you to explore and query the database content.

### Contribution
We welcome contributions! If you have suggestions or improvements, please open an issue or submit a pull request.
