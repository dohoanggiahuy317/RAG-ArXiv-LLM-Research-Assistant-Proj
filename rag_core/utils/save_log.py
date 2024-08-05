import os

def save_log(content, file_path):
    try:
        # Ensure the directory exists
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the content to the file
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Content successfully saved to {file_path}")

    except Exception as e:
        print(f"An error occurred while saving the content: {e}")

def add_log(content, file_path):
    try:
        # Ensure the directory exists
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Append the content to the file
        with open(file_path, 'a') as file:
            file.write(content + '\n')  # Append content with a newline
        print(f"Content successfully appended to {file_path}")

    except Exception as e:
        print(f"An error occurred while saving the content: {e}")
