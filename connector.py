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

    def create_data_group(self, group_name : str) -> str:
        """Create data group in Cloud DFS

        :param group_name: group name :str
        :return: a token of group :str
        """
        url = self._url + '/group'
        print("Connected URL :", url)

        r = requests.post(url, json={
            'name': group_name
        })

        if r.status_code == 201:
            pass
        else:
            raise UnknownError('Unknown error code of requests. HTTP Status Code : {0}'.format(r.status_code))

        result = r.json()
        return result['token']

    def get_data_group_info(self, group_token : str) -> dict:
        """Get a information of data group in Cloud DFS.

        :param group_token: a token of group :str
        :return: a dictionary for the information :dict
            example) {
                'name': 'the name of data group',
                'data_token_list': [
                    'a_token_of_data_1_in_group', 'a_token_of_data_2_in_group',
                    ..., ''a_token_of_data_N_in_group''
                ]
            }
        """
        url = self._url + '/group/' + group_token
        print("Connected URL :", url)

        r = requests.get(url)

        if r.status_code == 200:
            pass
        elif r.status_code == 404:
            raise NotFoundError('There is no data group which has given token.')
        else:
            raise UnknownError('Unknown error code of requests. HTTP Status Code : {0}'.format(r.status_code))

        return r.json()

    def remove_data_group(self, group_token : str):
        """Delete data file in Cloud DFS

            :param group_token: a token for data group :str
            :return: None
        """
        url = self._url + '/group/' + group_token
        print("Connected URL :", url)
        r = requests.delete(url)

        if r.status_code == 204:
            pass
        elif r.status_code == 404:
            raise NotFoundError('There is no data group which has given token.')
        else:
            raise UnknownError('Unknown error code of requests. HTTP Status Code : {0}'.format(r.status_code))

    def put_data_file(self, name : str, data, data_type : str, group_token : str = None) -> str:
        """Put data file in Cloud DFS

        :param name: file name :str
        :param data: file data :str or bytes
        :param data_type: data type :str ('text' or 'binary')
        :param group_token: group token :str
        :return: a token of file :str
        """
        if data_type != 'binary' and data_type != 'text':
            raise ParamError('Invalid data_type.')

        url = self._url + '/data'
        print("Connected URL :", url)

        if data_type == 'binary':
            if group_token is None:
                form_data = None
            else:
                form_data = {
                    'group_token': group_token
                }
            r = requests.post(url, files={
                'data': (name, data)
            }, data=form_data)
        else: # text
            json_data = {
                'name': name,
                'data': data
            }
            if group_token is not None:
                json_data['group_token'] = group_token
            r = requests.post(url, json=json_data)

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
        """Delete data file in Cloud DFS

        :param token: a token for data file :str
        :return: None
        """
        url = self._url + '/data/' + token
        print("Connected URL :", url)
        r = requests.delete(url)

        if r.status_code == 204:
            pass
        elif r.status_code == 404:
            raise NotFoundError('There is no data file which has given token.')
        else:
            raise UnknownError('Unknown error code of requests. HTTP Status Code : {0}'.format(r.status_code))
