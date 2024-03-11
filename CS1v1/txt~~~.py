import json
import os
import re

def sanitize_filename(url):
    """
    Sanitizes the URL to be used as a valid filename by removing or replacing invalid characters.
    """
    # Remove the protocol (http, https) and replace invalid characters with underscores
    sanitized = re.sub(r'https?://', '', url)  # Remove protocol
    sanitized = re.sub(r'[^a-zA-Z0-9\-_\.]', '_', sanitized)  # Replace invalid chars with _
    return sanitized

def save_json_items_as_txt(file_path, output_directory):
    # Load the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Loop through each item in the JSON data
    for index, item in enumerate(data):
        # Extract the URL and sanitize it to be used as a filename
        sanitized_filename = sanitize_filename(item['url'])
        # Limit the filename length to avoid filesystem errors, optionally add an index to ensure uniqueness
        sanitized_filename = sanitized_filename[:50] + f"_{index}.txt"
        new_file_path = os.path.join(output_directory, sanitized_filename)
        
        # Save each item to a separate TXT file in the specified directory
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            # Convert the dictionary to a pretty-printed string and write it to a file
            json_str = json.dumps(item, ensure_ascii=False, indent=4)
            new_file.write(json_str)
            
        print(f'Saved: {new_file_path}')

# Define the path to your JSON file and the output directory
json_file_path = 'CS_Data_1v1.json'  # Adjust this to the path where your JSON file is located
output_dir = '/home/enoc2/hyj/CS_single_version/CS1v1_txt'  # The directory where you want to save the TXT files

# Execute the function with the specified paths
save_json_items_as_txt(json_file_path, output_dir)
