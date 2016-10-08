import os
from cloud_dfs.library import SingletonMeta


class Error(Exception):
    pass

class ParamError(Error):
    pass


class FileManager(metaclass=SingletonMeta):

    def __init__(self, root_dir : str):
        if not os.path.isabs(root_dir):
            raise ParamError('root_dir must be given by absolute directory.')
        self._ensure_dir(root_dir)
        self._root_dir = root_dir

    def _ensure_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def store(self, filename : str, file_data):
        file_path = os.path.join(self._root_dir, filename)
        try:
            if type(file_data) is bytes:
                mode = 'wb'
            elif type(file_data) is str:
                mode = 'wt'
            else:
                raise ParamError('{0} is not supported type.'.format(type(file_data)))
            with open(file_path, mode) as f:
                f.write(file_data)
        except OSError:
            raise ParamError('can\'t access to given file("{0}")'.format(file_path))
        return file_path

    def remove(self, file_path):
        try:
            os.remove(file_path)
        except FileNotFoundError as e:
            raise ParamError('invalid file_path. ' + str(e))
