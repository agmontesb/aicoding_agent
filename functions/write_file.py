import os

from functions.config import FunctionError, check_working_directory


def write_file(working_directory, file_path, content):
    try:
        file_path = check_working_directory(working_directory, file_path)
    except FunctionError as e:
        return str(e)
    
    if not file_path.is_file():
        return f'ERROR: "{file_path}" is not a file'

    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f'Succesfully wrote "{file_path}": {len(content)} characters.'
    except Exception as e:
        return f'ERROR: {str(e)}'