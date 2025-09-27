import subprocess
from google.genai import types as genai_types

from functions.config import FunctionError, check_working_directory, TIMED_OUT


def run_python_file(working_directory, file_path, args=None):
    try:
        file_path = check_working_directory(working_directory, file_path)
        if not file_path.exists():
            raise FunctionError('ERROR: {file_path} not found')
        if not file_path.is_file():
            raise FunctionError(f'ERROR: "{file_path}" is not a file')
        if file_path.suffix != '.py':
            raise FunctionError(f'ERROR: "{file_path}" is not a Python file')
    except FunctionError as e:
        return str(e)

    
    working_directory = check_working_directory(working_directory, '')
    args = args or []
    try:
        output = subprocess.run(
            ['python', file_path, *args],
            cwd=working_directory, 
            timeout=TIMED_OUT, 
            capture_output=True,
        )
        to_return = []
        if not output.stdout and not output.stderr:
            to_return.append(f'No output produced')
        else:
            to_return.append(f'STDOUT:{output.stdout}')
            to_return.append(f'STDERR:{output.stderr}')
        if output.returncode != 0:
            to_return.append(f'Process exited with code: {output.returncode}')
        return '\n'.join(to_return)
    except Exception as e:
        return f'ERROR: executing python file: {str(e)}'


schema_run_python_file = genai_types.FunctionDeclaration(
    name='run_python_file',
    description='Run the given python file (.py) with the python3 interpreter, accepts aditional CLI arguments as an optional array',
    parameters=genai_types.Schema(
        type=genai_types.Type.OBJECT,
        properties={
            'file_path': genai_types.Schema(
                type=genai_types.Type.STRING,
                description='The relative path of the file to run, path relative to the working directory.',
            ),
            'args': genai_types.Schema(
                type=genai_types.Type.ARRAY,
                items=genai_types.Schema(
                    type=genai_types.Type.STRING,
                ),
                description='Arguments to pass as part of sys.argv to the python file. Optional.',
            ),
        },
        required=['file_path'],
    ),
)



if __name__ == '__main__':
    working_directory = 'calculator'
    file_path = 'main.py'
    print(run_python_file(working_directory, file_path, ['2 + 3*(1+4)']))

