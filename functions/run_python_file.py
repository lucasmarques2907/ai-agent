import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a specified Python file with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Name of the file"
                },
                "args": {
                    "type": "array",
                    "description": "array of optional arguments",
                    "items": {
                        "type": "string",
                    }
                }
            },
            "required": [
                "file_path"
            ]
        }
    }
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs]
        if(args != None):
            command.extend(args)
        completed_process: subprocess.CompletedProcess = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        
        output: list[str] = []
        
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stdout and not completed_process.stderr:
            output.append("No output produced")
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")
        
        return ("\n").join(output)
    except Exception as err:
        return f"Error: executing Python file: {err}"
    
print(run_python_file("calculator", "main.py"))