document.addEventListener('DOMContentLoaded', function () {
    // Global Modal Elements
    const modals = {
        globalSettingsPopup: document.getElementById('global_settings_popup'),
        finetuneEmbedderPopup: document.getElementById('finetune_embedder_popup'),
        saveDocsPopup: document.getElementById('save_docs_popup'),
        changeUserPopup: document.getElementById('change_user_popup'),
        chatConfigPopup: document.getElementById('chat_config_popup')
    };

    // Buttons
    const buttons = {
        globalSettingsBtn: document.getElementById('fetch_data_btn'),
        finetuneEmbedderBtn: document.getElementById('finetune_embedder_btn'),
        saveDocsBtn: document.getElementById('save_docs_btn'),
        changeUserBtn: document.getElementById('change_user_btn'),
        chatConfigBtn: document.getElementById('chat_config_btn'),
        closeButtons: document.querySelectorAll('.close')
    };

    let currentUserId = null;

    // Show processing message and disable all buttons
    function showProcessingMessage() {
        const processingDiv = document.getElementById('processing');
        processingDiv.textContent = 'Processing...';
        processingDiv.style.display = 'flex';

        // Disable all buttons to prevent further actions
        Object.values(buttons).forEach(button => {
            if (Array.isArray(button)) {
                button.forEach(btn => btn.disabled = true);
            } else {
                button.disabled = true;
            }
        });
    }

    // Hide processing message and enable all buttons
    function hideProcessingMessage() {
        const processingDiv = document.getElementById('processing');
        processingDiv.textContent = '';
        processingDiv.style.display = 'none';

        // Enable all buttons
        Object.values(buttons).forEach(button => {
            if (Array.isArray(button)) {
                button.forEach(btn => btn.disabled = false);
            } else {
                button.disabled = false;
            }
        });
    }

    // ======================================================================================
    // ================================  UPDATE STATUS  =====================================
    // ======================================================================================

    function updateStatus() {
        return fetch('/get_current_status')
            .then(response => response.json())
            .then(data => {
                const compressorType = data.compressor_type === 1 ? 'LLM FILTER' : 'LLM EXTRACT';
                document.getElementById('compressor_type_status').textContent = compressorType;
                document.getElementById('vector_db_name_status').textContent = data.vector_db_name || 'N/A';
                document.getElementById('user_id_status').textContent = data.user_id || 'N/A';
                document.getElementById('conversation_id_status').textContent = data.conversation_id;
                document.getElementById('k_status').textContent = data.k;
                document.getElementById('embedding_type_status').textContent = data.embedding_type;
                document.getElementById('embedder_name_status').textContent = data.embedder_name || 'N/A';
            })
            .catch(error => {
                console.error('Error fetching status:', error);
            });
    }

    updateStatus()

    // ======================================================================================
    // ================================  OPEN WINDOW  =======================================
    // ======================================================================================

    // Event Listeners for opening modals
    buttons.globalSettingsBtn.addEventListener('click', function () {
        modals.globalSettingsPopup.style.display = 'block';
    });

    buttons.finetuneEmbedderBtn.addEventListener('click', function () {
        modals.finetuneEmbedderPopup.style.display = 'block';
    });

    buttons.saveDocsBtn.addEventListener('click', function () {
        modals.saveDocsPopup.style.display = 'block';
    });

    buttons.changeUserBtn.addEventListener('click', function () {
        modals.changeUserPopup.style.display = 'block';
    });

    buttons.chatConfigBtn.addEventListener('click', function () {
        modals.chatConfigPopup.style.display = 'block';
        loadVectorDBOptions();
    });

    // Close modal when clicking the close button
    buttons.closeButtons.forEach(button => {
        button.addEventListener('click', function () {
            closeAllModals();
        });
    });

    // Close modal if user clicks outside the modal content
    window.addEventListener('click', function (event) {
        Object.values(modals).forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Helper Function to Close All Modals
    function closeAllModals() {
        Object.values(modals).forEach(modal => modal.style.display = 'none');
    }

    // ======================================================================================
    // ====================================  FETCH DATA  ====================================
    // ======================================================================================

    document.getElementById('fetch_data_form').addEventListener('submit', function (event) {
        event.preventDefault();

        showProcessingMessage();

        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());

        fetch('/fetch_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(response => response.json()).then(data => {
            hideProcessingMessage();
            statusDiv.textContent = data.status === 'success' ? 'Data fetched successfully.' : 'Error fetching data.';
            updateStatus();  // Update status after fetching data
        }).catch(() => {
            hideProcessingMessage();
            statusDiv.textContent = 'Error fetching data.';
        });
    });

    // ======================================================================================
    // =============================  FINETUNE EMBEDDER  ====================================
    // ======================================================================================

    document.getElementById('finetune_embedder_form').addEventListener('submit', function (event) {
        event.preventDefault();

        showProcessingMessage();

        const embedderName = document.getElementById('embedder_name').value.trim();

        if (!embedderName) {
            alert('embedderName is required');
            return;
        }

        fetch('/finetune_embedder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ embedder_name: embedderName })
        }).then(response => response.json()).then(data => {
            hideProcessingMessage();
            statusFinetune.textContent = data.message;
            updateStatus();  // Update status after finetuning embedder
        }).catch(() => {
            hideProcessingMessage();
            statusFinetune.textContent = 'Error finetuning embedder.';
        });
    });

    // ======================================================================================
    // =================================  SAVE DOCS  =======================================
    // ======================================================================================

    document.getElementById('save_docs_form').addEventListener('submit', function (event) {
        event.preventDefault();

        const vectorDBName = document.getElementById('vector_db_name').value.trim();
        const embedderName = document.getElementById('custom_embedder_name').value.trim();
        const embedderType = document.getElementById('embedder_type').value.trim();

        if (!vectorDBName) {
            alert('vectorDBName is required');
            return;
        }
        
        showProcessingMessage();

        fetch('/save_docs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                embedder_type: embedderType,
                embedder_name: embedderName,
                vector_db_name: vectorDBName
            })
        }).then(response => response.json()).then(data => {
            hideProcessingMessage();
            statusFinetune.textContent = data.message;
        }).catch(() => {
            hideProcessingMessage();
            statusFinetune.textContent = 'Error saveing docs to database.';
        });
    });

    // ======================================================================================
    // ================================  CUSTOM EMBEDDER  ===================================
    // ======================================================================================

    // Load Custom Embedder Options
    function loadCustomEmbedderOptions() {
        fetch('/get_custom_embedders')
            .then(response => response.json())
            .then(data => {
                const customEmbedderNameSelect = document.getElementById('custom_embedder_name');
                customEmbedderNameSelect.innerHTML = '';
                data.embedders.forEach(embedder => {
                    const option = document.createElement('option');
                    option.value = embedder;
                    option.textContent = embedder;
                    customEmbedderNameSelect.appendChild(option);
                });
            });
    }

    // Show/Hide Custom Embedder Options
    document.getElementById('embedder_type').addEventListener('change', function () {
        const customEmbedderOptions = document.getElementById('custom_embedder_options');
        if (this.value === 'custom') {
            customEmbedderOptions.style.display = 'block';
            loadCustomEmbedderOptions();
        } else {
            customEmbedderOptions.style.display = 'none';
        }
    });


    // ======================================================================================
    // ===================================  VECTOR DB  ======================================
    // ======================================================================================

    // Load Custom Embedder Options
    function loadVectorDBOptions() {
        fetch('/get_vector_db')
            .then(response => response.json())
            .then(data => {
                const vectorDBSelect = document.getElementById('vector_db_name_chat');
                vectorDBSelect.innerHTML = '';
                data.vectorDBs.forEach(vectorDB => {
                    const option = document.createElement('option');
                    option.value = vectorDB;
                    option.textContent = vectorDB;
                    vectorDBSelect.appendChild(option);
                });
            });
    }


    // ======================================================================================
    // ==================================  CHANGE USER  =====================================
    // ======================================================================================

    // Handle Change User
    document.getElementById('save_user_btn').addEventListener('click', function (event) {
        event.preventDefault();

        const userId = document.getElementById('new_user_id').value.trim();

        console.log(userId)
        if (!userId) {
            alert('userId is required');
            return;
        }

        if (userId) {
            currentUserId = userId;
            loadChatThreads(userId);
            closeAllModals();
        }
        setTimeout(updateStatus, 0);

        fetch(`/get_max_conversation_id/${currentUserId}`)
        .then(response => response.json())
        .then(data => {
            // Increment the max_id by 1 to create a new thread
            currentConversationId = data.max_id + 1;

            // Clear the chat window for the new thread
            document.getElementById('chat_window').innerHTML = '';
        }).then(
            () => {updateStatus()}
        );


    });

    // ======================================================================================
    // ================================  CHAT CONFIG  =======================================
    // ======================================================================================

    document.getElementById('chat_config_form').addEventListener('submit', function (event) {
        event.preventDefault();

        showProcessingMessage();

        const compressorType = document.getElementById('compressor_type').value.trim();
        const vectorDBName = document.getElementById('vector_db_name_chat').value.trim();


        fetch('/chat_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                compressor_type: compressorType,
                vector_db_name: vectorDBName
            })
        }).then(response => response.json()).then(data => {
            hideProcessingMessage();
            statusFinetune.textContent = data.message;
        }).catch(() => {
            hideProcessingMessage();
            statusFinetune.textContent = 'Error saveing docs to database.';
        });
        setTimeout(updateStatus, 0);
        closeAllModals()
    });



    // ======================================================================================
    // ==================================  CHAT THREAD  =====================================
    // ======================================================================================
    // Load chat threads for the user
    function loadChatThreads(userId) {
        fetch(`/get_chat_threads/${userId}`)
            .then(response => response.json())
            .then(data => {
                const chatThreadsList = document.getElementById('chat_threads');
                chatThreadsList.innerHTML = ''; // Clear existing threads
                data.threads.forEach(thread => {
                    const li = document.createElement('li');
                    li.textContent = `Thread ${thread.conversation_id}`;
                    li.dataset.conversationId = thread.conversation_id;
                    li.addEventListener('click', function () {
                        loadChatMessages(thread.conversation_id);
                    });
                    chatThreadsList.appendChild(li);
                });
            }).then(
                // Now update the status after threads are loaded
                updateStatus()
            );
    }

    // Load chat messages for a thread
    function loadChatMessages(conversationId) {
        fetch(`/get_chat_messages/${currentUserId}/${conversationId}`)
            .then(response => response.json())
            .then(data => {
                const chatWindow = document.getElementById('chat_window');
                chatWindow.innerHTML = ''; // Clear existing messages
                data.messages.forEach(msg => {
                    const messageType = msg.type === 'human' ? 'human' : 'ai';
                    const formattedContent = formatContent(msg.data.content);

                    chatWindow.innerHTML += `<div class="message ${messageType}"><strong>${messageType === 'human' ? 'You' : 'Assistant'}:</strong> ${formattedContent}</div>`;
                });
            }).then(
                updateStatus()
            );
    }

    // Function to format the content by converting \n into line breaks and handling special formats
    function formatContent(content) {
        return content.replace(/\n/g, '<br>').replace(/\t/g, '&emsp;');
    }




    // ======================================================================================
    // ===================================  CHAT WINDOW  ====================================
    // ======================================================================================

    document.getElementById('send').addEventListener('click', function () {
        const userInput = document.getElementById('user_input').value;
        
        if (userInput.trim() === '') return;
    
        const chatWindow = document.getElementById('chat_window');
        
        // Show user input on the right
        chatWindow.innerHTML += `<div class="message human"><strong>You:</strong> ${userInput}</div>`;
        
        // Show processing message on the left
        chatWindow.innerHTML += `<div class="message ai" id="processing_message"><strong>Assistant:</strong> Thinking about your question. Please wait 🤗. In the mean time, please check the terminal to see the process. <br> Tips: Recored the references at the end of my responses, or you can find it later in the log file under  chat_core/logs/{username)-{chat_id}/compressor_{no}/info...</div>`;
        
        // Clear the input field
        document.getElementById('user_input').value = '';

        // Disable input and send button
        document.getElementById('user_input').disabled = true;
        document.getElementById('send').disabled = true;
    
        // Send the input to the backend
        fetch('/process_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Remove processing message and show the response
            const processingMessage = document.getElementById('processing_message');
            processingMessage.remove();
            
            let sources = '';
            if (data.source && data.source.length > 0) {
                sources = `<br><em>Sources: ${data.source.join(', ')}</em>`;
            }
    
            chatWindow.innerHTML += `<div class="message ai"><strong>Assistant:</strong> ${data.response}<br>${sources}</div>`;
            
            // Re-enable input and send button
            document.getElementById('user_input').disabled = false;
            document.getElementById('send').disabled = false;
            
            // Clear the input field
            document.getElementById('user_input').value = '';

            loadChatThreads(currentUserId);
        })
        .catch(error => {
            console.error('Error processing message:', error);
            
            // Handle the error, re-enable input and send button
            document.getElementById('user_input').disabled = false;
            document.getElementById('send').disabled = false;
            
            // Update processing message with an error message
            const processingMessage = document.getElementById('processing_message');
            processingMessage.innerHTML = '<strong>Assistant:</strong> Error processing your message. Please try again.';
        });
    });

    document.getElementById('new_thread').addEventListener('click', function () {
        // Fetch the current max conversation_id from the server
        fetch(`/get_max_conversation_id/${currentUserId}`)
            .then(response => response.json())
            .then(data => {
                // Increment the max_id by 1 to create a new thread
                currentConversationId = data.max_id + 1;

                // Clear the chat window for the new thread
                document.getElementById('chat_window').innerHTML = '';
            }).then(
                () => {updateStatus()}
            );
    });


});