import unittest


class MyTestCase(unittest.TestCase):

    def test_connector(self):
        from connector import CloudDFSConnector, Error, NotFoundError, UnknownError, UnprocessableError

        conn = CloudDFSConnector('127.0.0.1', 5000)

        help_msg = conn.help()
        print(help_msg)

        test_name = [
            'Test File #1', 'Test File #2', 'Test File #3'
        ]
        test_data = [
            b'Test Data #1', 'Test Data #2', b'Test Data #3'
        ]
        test_data_type = [
            'binary', 'text', 'binary'
        ]
        tokens = []

        token = conn.put_data_file(test_name[0], test_data[0], test_data_type[0])
        tokens.append(token)
        print(token)

        token = conn.put_data_file(test_name[1], test_data[1], test_data_type[1])
        tokens.append(token)
        print(token)

        name, data = conn.get_data_file(tokens[0])
        self.assertEqual(name, test_name[0])
        self.assertEqual(data, test_data[0])

        name, data = conn.get_data_file(tokens[1])
        self.assertEqual(name, test_name[1])
        self.assertEqual(data, test_data[1])

        conn.del_data_file(tokens[0])

        try:
            name, data = conn.get_data_file(tokens[0])
        except NotFoundError:
            pass
        else:
            self.assertEqual(True, False)

        token = conn.put_data_file(test_name[2], test_data[2], test_data_type[2])
        tokens.append(token)
        print(token)

        name, data = conn.get_data_file(tokens[2])
        self.assertEqual(name, test_name[2])
        self.assertEqual(data, test_data[2])

        try:
            conn.del_data_file(tokens[0])
        except NotFoundError:
            pass
        else:
            self.assertEqual(True, False)

        conn.del_data_file(tokens[1])
        conn.del_data_file(tokens[2])


if __name__ == '__main__':
    unittest.main()
