from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from parse_data.code.collect_data.parse_data import fetch_papers
from rag_core.utils.embedding import load_embedding_model, fine_tune_model
from chatcore.utils import load_chat_history, save_chat_history, generate_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    user_id = request.form['user_id']
    thread_id = request.form['thread_id']
    
    # Load the chat history and process the input
    history = load_chat_history(user_id, thread_id)
    response = generate_response(user_input, history)
    
    # Save chat history
    save_chat_history(user_id, thread_id, user_input, response)
    
    return jsonify({'response': response})

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        embedding_model = request.form['embedding_model']
        fine_tune_option = request.form.get('fine_tune', False)
        
        # Update the embedding model
        load_embedding_model(embedding_model)
        
        if fine_tune_option:
            # Fine-tune the model
            fine_tune_model()
        
        return redirect(url_for('settings'))
    
    # Get available models for selection
    available_models = ["Model1", "Model2", "Model3"]  # Replace with actual model names
    return render_template('settings.html', models=available_models)

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    # Fetch new papers from the parse_data folder
    fetch_papers()
    return jsonify({'status': 'success'})

@app.route('/change_user', methods=['POST'])
def change_user():
    user_id = request.form['user_id']
    thread_id = request.form['thread_id']
    # Load the user's chat history
    history = load_chat_history(user_id, thread_id)
    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(debug=True)