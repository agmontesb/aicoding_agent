import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types

from functions.get_file_info import schema_get_file_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from call_function import call_function



# Carga las variables de entorno desde el archivo .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    equivs = {'-v': '--verbose'}
    bflags = dict(verbose=False)
    client = genai.Client(api_key=api_key)

    system_prompt = '''
    You are a usesful coding agent.
     
    When the user asks a question or make a request, make a function call plan. You can perform the following operations:
    
    - List files and directories.
    - Read  the content of a file.
    - Wtite to a file (create or update).
    - Run a python file with optional arguments.
    

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. 
     
    
    '''

    if len(sys.argv) < 2:
        prompt = input("Please enter a prompt or type QUIT to exit:  ")
        if prompt.upper() == "QUIT":
            sys.exit(0)
        prompt = prompt.strip()
    else:
        args = sys.argv[1:]
        while True:
            item, *args = args
            if not args:
                break
            key = equivs.get(item, item)[2:]
            bflags[key] = True
        prompt = item

    messages = [
        genai_types.Content(role="user", parts=[genai_types.Part(text=prompt)])
    ]

    available_functions = genai_types.Tool(
        function_declarations=[
            schema_get_file_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    config = genai_types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions],
    )
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages, 
        config=config,
    )

    if response is None or response.usage_metadata is None:
        print("Response is malformed")
        return

    if bflags['verbose']:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Completion tokens: {response.usage_metadata.candidates_token_count}')
        print(f'Total tokens: {response.usage_metadata.total_token_count}')

    if response.function_calls:
        for function_call_part in response.function_calls:
            # print(f'Calling function: {function_call_part.name}({function_call_part.args})')
            result = call_function(function_call_part, bflags['verbose'])
            print(result)
    else:
        print(response.text)


if __name__ == "__main__":
    main()
