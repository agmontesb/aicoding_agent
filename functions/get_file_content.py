import os
import pathlib

from config import MAX_CHARS, FunctionError, check_working_directory


def get_file_content(working_directory, file_path):
    try:
        file_path = check_working_directory(working_directory, file_path)
    except FunctionError as e:
        return str(e)
    
    if not file_path.exists():
        raise f'ERROR: {file_path} not found'

    if not file_path.is_file():
        return f'ERROR: "{file_path}" is not a file'
    
    file_size = file_path.stat().st_size

    try:
        with open(file_path, 'r') as f:
            content = f.read(MAX_CHARS)
    except Exception as e:
        return f'ERROR: {str(e)}'
    
    if file_size > MAX_CHARS:
        content += f'[... File "{file_path}" truncated at {MAX_CHARS} characters].'
    return content


if __name__ == '__main__':
    content = get_file_content('calculator', 'lorem.txt')
    print(content)

