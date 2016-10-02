import requests


class Error(Exception):
    pass

class UnprocessableError(Error):
    pass

class NotFoundError(Error):
    pass

class UnknownError(Error):
    pass


class CloudDFSConnector(object):

    def __init__(self, ip : str, port : int):
        self._ip = ip
        self._port = port
        self._url = 'http://{0}:{1}'.format(ip, port)

    def help(self):
        url = self._url + '/help'
        print("Connected URL :", url)
        r = requests.get(url)

        if r.status_code == 200:
            pass
        else:
            raise UnknownError('Unknown error code of requests. HTTP Status Code : {0}'.format(r.status_code))

        return r.json()

    def put_data_file(self, name : str, data : bytes):
        url = self._url + '/data'
        print("Connected URL :", url)
        r = requests.post(url, files={
            'data': (name, data)
        })

        if r.status_code == 201:
            pass
        elif r.status_code == 422:
            raise UnprocessableError('A server cannot create a data file.')
        else:
            raise UnknownError('Unknown error code of requests. HTTP Status Code : {0}'.format(r.status_code))

        result = r.json()
        return result['token']

    def get_data_file(self, token : str) -> bytes:
        url = self._url + '/data/' + token
        print("Connected URL :", url)
        r = requests.get(url)

        if r.status_code == 200:
            pass
        elif r.status_code == 404:
            raise NotFoundError('There is no data file which has given token.')
        else:
            raise UnknownError('Unknown error code of requests. HTTP Status Code : {0}'.format(r.status_code))

        return r.content

    def del_data_file(self, token : str):
        url = self._url + '/data/' + token
        print("Connected URL :", url)
        r = requests.delete(url)

        if r.status_code == 204:
            pass
        elif r.status_code == 404:
            raise NotFoundError('There is no data file which has given token.')
        else:
            raise UnknownError('Unknown error code of requests. HTTP Status Code : {0}'.format(r.status_code))
