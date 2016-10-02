import requests
import cgi


class Error(Exception):
    pass

class ParamError(Error):
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

    def put_data_file(self, name : str, data, data_type : str) -> str:
        """Put data file in Cloud DFS

        :param name: file name :str
        :param data: file data :str or bytes
        :param data_type: data type :str ('text' or 'binary')
        :return: a token of file :str
        """

        if data_type != 'binary' and data_type != 'text':
            raise ParamError('Invalid data_type.')

        url = self._url + '/data'
        print("Connected URL :", url)

        if data_type == 'binary':
            r = requests.post(url, files={
                'data': (name, data)
            })
        else: # text
            r = requests.post(url, json={
                'name': name,
                'data': data
            })

        if r.status_code == 201:
            pass
        elif r.status_code == 422:
            raise UnprocessableError('A server cannot create a data file.')
        else:
            raise UnknownError('Unknown error code of requests. HTTP Status Code : {0}'.format(r.status_code))

        result = r.json()
        return result['token']

    def get_data_file(self, token : str):
        """Get data file in Cloud DFS

        :param token: a token of file :str
        :return: (file name, file data) :tuple
        """

        url = self._url + '/data/' + token
        print("Connected URL :", url)
        r = requests.get(url)

        if r.status_code == 200:
            pass
        elif r.status_code == 404:
            raise NotFoundError('There is no data file which has given token.')
        else:
            raise UnknownError('Unknown error code of requests. HTTP Status Code : {0}'.format(r.status_code))

        content_type = r.headers.get('Content-Type')
        if 'application/json' in content_type:  # text data
            result = r.json()
            return result['name'], result['data']
        elif 'application/octet-stream' in content_type:  # binary data
            h = r.headers.get('Content-Disposition')
            value, params = cgi.parse_header(h)
            return params['filename'], r.content
        else:
            raise UnknownError('Server reply invalid http message.')

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
