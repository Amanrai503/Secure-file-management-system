import os

def get_folder_structure(directory):
    structure = []
    
    try:
        items = os.listdir(directory)  # List all items
        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):  # Only process folders
                structure.append([item, get_folder_structure(item_path)])  
    except PermissionError:
        pass  # Skip folders without permission
    
    return structure

# Example usage
folder_path = "D:/python/Secure File Management System/Drive"  # Change this to your directory
nested_folders = get_folder_structure(folder_path)
print(nested_folders)

['test'['test2']]
