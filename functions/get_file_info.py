import os

from config import check_working_directory, FunctionError


def get_file_info(working_directory, directory=''):
    try:
        file_path = check_working_directory(working_directory, directory)
    except FunctionError as e:
        return str(e)

    if not file_path.exists():
        raise f'ERROR: {file_path} not found'

    info = []
    fnc = lambda x, bflag=False: f'- {os.path.basename(x)}: file_size={os.path.getsize(x)} bytes, is_dir={bflag}'
    root, dirs, files = next(file_path.walk())
    [
        info.append(fnc(os.path.join(root, file)))
        for file in files
    ]
    [
        info.append(fnc(os.path.join(root, dir), True))
        for dir in dirs
    ]
    return '\n'.join(info)

if __name__ == '__main__':
    working_directory = os.getcwd()
    print(get_file_info('calculator'))