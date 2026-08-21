import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write the content received to a file, changing the old content for the new. If the file does not exist, it is created.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Name of the file"
                },
                "content": {
                    "type": "string",
                    "description": "Content of the file to be written"
                }
            },
            "required": [
                "file_path",
                "content"
            ]
        }
    }
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        dir_name = os.path.dirname(file_path_abs)
        os.makedirs(dir_name, exist_ok=True)
        
        with open(file_path_abs, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as err:
        return f"Error: {err}"