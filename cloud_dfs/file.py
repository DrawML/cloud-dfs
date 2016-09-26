import os
from cloud_dfs.library import AutoIncrementEnum, SingletonMeta


class FileValueError(ValueError):
    def __init__(self, msg=''):
        self._msg = msg

    def __str__(self):
        return "FileValueError : %s" % self._msg


class FileManager(metaclass=SingletonMeta):

    def __init__(self, root_dir : str):
        if not os.path.isabs(root_dir):
            raise FileValueError('root_dir must be given by absolute directory.')
        root_dir = os.path.dirname(root_dir + '/')
        print(root_dir)
        self._ensure_dir(root_dir + '/')
        self._root_dir = root_dir

    def _ensure_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    # exception handling will be added.
    def store(self, filename : str, file_data : str):
        file_path = self._root_dir + '/' + filename
        with open(file_path, 'w') as f:
            f.write(file_data)
        return file_path

    def remove(self, file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            raise FileValueError('invalid file_path. ' + str(e))
