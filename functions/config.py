import pathlib

MAX_CHARS = 10000


class FunctionError(Exception):
    pass


def check_working_directory(working_directory, file_path):
    base_path = pathlib.Path(working_directory).resolve()
    if file_path:
        file_path = base_path / file_path
    else:
        file_path = base_path
    file_path = file_path.resolve()
    
    if not file_path.is_relative_to(base_path):
        raise FunctionError(f'ERROR: "Cannot read "{file_path}" as it is outside of "{base_path}"')
    
    return file_path



