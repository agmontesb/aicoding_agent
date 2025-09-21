import os
from google.genai import types as genai_types

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
    

schema_write_file = genai_types.FunctionDeclaration(
    name='write_file',
    description='Overwrites an existing file or writes to a new file if it does not exists creating required path directories as needed, constrained to the working directory',
    parameters=genai_types.Schema(
        type=genai_types.Type.OBJECT,
        properties={
            'file_path': genai_types.Schema(
                type=genai_types.Type.STRING,
                description='The path of the file to write the content to, relative to the working directory.',
            ),
            'content': genai_types.Schema(
                type=genai_types.Type.STRING,
                description='The content to write to the file.',
            ),
        },
        required=['file_path', 'content'],
    ),
)
