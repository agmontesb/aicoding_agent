from google.genai import types as genai_types

from functions.get_file_info import get_file_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content



working_directory = 'calculator'


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f'Calling function: {function_call_part.name}({function_call_part.args})')
    else:
        print(f'Calling function: {function_call_part.name}')

    if function_call_part.name == 'get_file_info':
        response = get_file_info(working_directory, **function_call_part.args)
    elif function_call_part.name == 'get_file_content':
        response = get_file_content(working_directory, **function_call_part.args)
    elif function_call_part.name == 'run_python_file':
        response = run_python_file(working_directory, **function_call_part.args)
    elif function_call_part.name == 'write_file':
        response = write_file(working_directory, **function_call_part.args)
    else:
        response = 'ERROR: Not a valid tool {function_call_part.name}' 

    if response.startswith('ERROR:'):
        return genai_types.Content(
            role='Tool',
            name=function_call_part.name,
            parts=[
                genai_types.Part(text=response)
            ]
        )
    else:
        print(response)