import os
import pyperclip


def cleanSource(folder_path=None):

    if folder_path is None:
        if pyperclip.paste().endswith('/'):
            folder_path = pyperclip.paste()
        else:
            folder_path = pyperclip.paste() + '/'

    # folder_path = os.path.dirname(folder_path)
    print(folder_path)

    for _root, _, _files in os.walk(folder_path):
        for filename in _files:
            _file_path = os.path.join(_root, filename)
            if filename == "__var_config.xml" or filename == "__config.xml" \
                    or filename == "maml.xml" or filename == "__maml.xml":
                print(f'Remove: {_file_path}')
                os.remove(_file_path)


if __name__ == "__main__":
    cleanSource()
