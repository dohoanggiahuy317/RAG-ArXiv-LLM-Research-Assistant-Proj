from flask import Flask, render_template, request, jsonify

import sqlite3
import json
import os

from parse_data.code.collect_data.parse_data import fetch_papers
from parse_data.code.collect_data.split_paper import split_paper_abstract
from finetune_embedder.code.data_prep import csv_2_label
from finetune_embedder.code.finetune import finetune_embedder
from rag_core.pipeline.save_docs import save_embedding
from chat_core.chatbot import chat

app = Flask(__name__)



# ======================================================================================
# ====================================  GLOBAL VAR  ====================================
# ======================================================================================

# Global variable to store embedder path
class DefaultVar():
    RAW_DATA_DIR="data"
    RAW_DATA_CSV_PATH = "data/papers_abstract.csv"
    
    FINETUNE_EMBEDDER_DATA_DIR = "finetune_embedder/data"
    FINETUNE_MODEL_DIR = "finetune_embedder/models/"

    ABSTRACT_DIR = "data/abstract"
    VECTOR_DATABASE_DIR = "database/rag_core/"

    DATABASE_VS_EMBEDDER_PATH="database/info.json"

class CurrentVal():
    EMBEDDING_TYPE = 1
    COMPRESSOR_TYPE = 1
    VECTOR_DB_NAME = ""
    EMBEDDER_NAME = None

    CONVERSATION_ID = 1
    USER_ID = None
    K = 3


@app.route('/get_current_status', methods=['GET'])
def get_current_status():
    data = load_json(DefaultVar.DATABASE_VS_EMBEDDER_PATH)
    embedder_name = data[CurrentVal.VECTOR_DB_NAME.split("/")[-1]] if CurrentVal.VECTOR_DB_NAME.split("/")[-1] in data else ""

    status = {
        'embedding_type': CurrentVal.EMBEDDING_TYPE,
        'compressor_type': CurrentVal.COMPRESSOR_TYPE,
        'vector_db_name': CurrentVal.VECTOR_DB_NAME.split("/")[-1],
        'embedder_name': embedder_name,
        'conversation_id': CurrentVal.CONVERSATION_ID,
        'user_id': CurrentVal.USER_ID,
        'k': CurrentVal.K,
    }
    return jsonify(status)


# ======================================================================================
# ====================================  MAIN INDEX  ====================================
# ======================================================================================


@app.route('/')
def index():
    return render_template('index.html')


# ======================================================================================
# ====================================  FETCH DATA  ====================================
# ======================================================================================

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    params = request.json
    start_index = int(params.get('start_index', 0))
    total_results = int(params.get('total_results', 10))
    results_per_iteration = int(params.get('results_per_iteration', 2))
    sort_by = params.get('sort_by', 'submittedDate')
    sort_order = params.get('sort_order', 'descending')
    wait_time = float(params.get('wait_time', 0.5))

    # Fetch new papers using the provided parameters
    fetch_papers(
        start_index=start_index,
        total_results=total_results,
        results_per_iteration=results_per_iteration,
        sort_by=sort_by,
        sort_order=sort_order,
        wait_time=wait_time,
        output_filename=DefaultVar.RAW_DATA_CSV_PATH
    )

    split_paper_abstract(
        csv_filepath=DefaultVar.RAW_DATA_CSV_PATH,
        output_dir=DefaultVar.RAW_DATA_DIR
    )

    return jsonify({'status': 'success'})


# ======================================================================================
# ================================  FINETUNE EMBEDDER  =================================
# ======================================================================================

@app.route('/finetune_embedder', methods=['POST'])
def finetune_embedder_route():

    csv_2_label(
        csv_filename=DefaultVar.RAW_DATA_CSV_PATH,
        output_dir=DefaultVar.FINETUNE_EMBEDDER_DATA_DIR
    )

    embedder_name = request.json.get('embedder_name')
    if embedder_name:
        # Call the finetune_embedder function with the specified name
        res, text = finetune_embedder(
            dataset_train_path=DefaultVar.FINETUNE_EMBEDDER_DATA_DIR + "/data_label.json",
            model_path=DefaultVar.FINETUNE_MODEL_DIR + embedder_name)
        
        if res:
            return jsonify({'status': 'success', 'message': f'Embedder {embedder_name} finetuned.'})
        return jsonify({'status': 'success', 'message': text})

    return jsonify({'status': 'error', 'message': 'Embedder name not provided.'})


# ======================================================================================
# =================================  CHOOSE EMBEDDER  ==================================
# ======================================================================================

@app.route('/get_custom_embedders')
def get_custom_embedders():
    embedder_directory = DefaultVar.FINETUNE_MODEL_DIR
    embedders = [f for f in os.listdir(embedder_directory) if os.path.isdir(os.path.join(embedder_directory, f))]
    return jsonify({'embedders': embedders})


@app.route('/get_vector_db')
def get_vector_DBs():
    vector_db_directory = DefaultVar.VECTOR_DATABASE_DIR
    vector_db = [f for f in os.listdir(vector_db_directory) if os.path.isdir(os.path.join(vector_db_directory, f))]
    return jsonify({'vectorDBs': vector_db})

# ======================================================================================
# =================================  SAVE DOCS  ========================================
# ======================================================================================

def load_json(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        # Create an empty JSON file with an empty dictionary
        with open(file_path, 'w') as json_file:
            json.dump({}, json_file)
    
    # Load the JSON file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    
    return data

def save_json(file_path, data):
    # Save the dictionary back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)



@app.route('/save_docs', methods=['POST'])
def save_docs_route():
    embedder_type = request.json.get('embedder_type')
    embedder_name = request.json.get('embedder_name')
    vector_db_name = request.json.get('vector_db_name')

    if embedder_type == 'custom':
        CurrentVal.EMBEDDING_TYPE = 2
    else:
        CurrentVal.EMBEDDING_TYPE = 1
        embedder_name = "default_BGE_small_en"
        
    # Call the save_docs function
    save_embedding(
        docs_dir=DefaultVar.ABSTRACT_DIR,
        db_path=DefaultVar.VECTOR_DATABASE_DIR + vector_db_name,
        embedding_type= CurrentVal.EMBEDDING_TYPE,
        model_path=DefaultVar.FINETUNE_MODEL_DIR + embedder_name
    )


    data = load_json(DefaultVar.DATABASE_VS_EMBEDDER_PATH)
    data[vector_db_name] = embedder_name
    save_json(DefaultVar.DATABASE_VS_EMBEDDER_PATH, data)


    return jsonify({'status': 'success', 'message': 'Documents saved to vector database.'})


# ======================================================================================
# ====================================  CHAT CONFIG  ===================================
# ======================================================================================


@app.route('/chat_config', methods=['POST'])
def update_chat_config():

    # Get from request
    compressor_type = request.json.get('compressor_type')
    vector_db_name = request.json.get('vector_db_name')

    # Update var
    CurrentVal.COMPRESSOR_TYPE = int(compressor_type)
    CurrentVal.VECTOR_DB_NAME = DefaultVar.FINETUNE_EMBEDDER_DATA_DIR + "/" + vector_db_name

    data = load_json(DefaultVar.DATABASE_VS_EMBEDDER_PATH)

    CurrentVal.EMBEDDER_NAME = data[vector_db_name]

    if CurrentVal.EMBEDDER_NAME == "default_BGE_small_en":
        CurrentVal.EMBEDDING_TYPE = 1
    else:
        CurrentVal.EMBEDDING_TYPE = 2

    return jsonify({'status': 'success', 'message': 'Saved config.'})


# ======================================================================================
# ====================================  CHAT CORE  =====================================
# ======================================================================================


def get_db_connection():
    conn = sqlite3.connect('database/chat_core/memory.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/get_chat_threads/<user_id>')
def get_chat_threads(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.execute('SELECT DISTINCT session_id FROM message_store WHERE session_id LIKE ?', (f'{user_id}--%',))
        threads = [{'session_id': row['session_id'], 'conversation_id': row['session_id'].split('--')[1]} for row in cursor.fetchall()]
        
        CurrentVal.USER_ID = user_id
        conn.close()

        return jsonify({'threads': threads})
    except Exception as e:
        CurrentVal.USER_ID = user_id
        return jsonify({'threads': []})

@app.route('/get_chat_messages/<user_id>/<conversation_id>')
def get_chat_messages(user_id, conversation_id):
    session_id = f'{user_id}--{conversation_id}'
    CurrentVal.CONVERSATION_ID = conversation_id

    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM message_store WHERE session_id = ?', (session_id,))
    
    messages = []
    for row in cursor.fetchall():
        message_data = json.loads(row['message'])
        message_type = message_data.get('type', 'human')
        message_content = message_data.get('data', {})
        messages.append({'type': message_type, 'data': message_content})

    conn.close()
    return jsonify({'messages': messages})




# ======================================================================================
# ===================================  CHAT WINDOW  ====================================
# ======================================================================================
@app.route('/process_message', methods=['POST'])
def process_message():
    user_message = request.json.get('message')
    if user_message:
        # Process the message (this function should exist in your chatbot.py)
        response, source = chat(
            question=user_message,
            compressor_type=CurrentVal.COMPRESSOR_TYPE,
            db_path=DefaultVar.VECTOR_DATABASE_DIR + CurrentVal.VECTOR_DB_NAME,
            user_id=CurrentVal.USER_ID,
            conversation_id=CurrentVal.CONVERSATION_ID,
            k=int(CurrentVal.K),
            embedding_type=CurrentVal.EMBEDDING_TYPE,
            model_path=DefaultVar.FINETUNE_MODEL_DIR + CurrentVal.EMBEDDER_NAME)
        print(source)
        return jsonify({'response': response, 'source': source})
    else:
        return jsonify({'error': 'No message received'}), 400

@app.route('/get_max_conversation_id/<user_id>', methods=['GET'])
def get_max_conversation_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.execute('SELECT DISTINCT session_id FROM message_store WHERE session_id LIKE ?', (f'{user_id}--%',))
        threads = [ int(row['session_id'].split('--')[1]) for row in cursor.fetchall()]
        
        CurrentVal.CONVERSATION_ID = max(threads) + 1 if len(threads) != 0 else 1
        
        conn.close()
        return jsonify({'max_id': CurrentVal.CONVERSATION_ID if len(threads) != 0 else 1})

    except Exception as e:
        return jsonify({'max_id': 1})



if __name__ == '__main__':
    app.run(debug=True, port=5000)