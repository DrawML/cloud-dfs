import unittest


class MyTestCase(unittest.TestCase):

    def test_data(self):
        """Test features only related in Data.
        """
        print("----------------- test_data ----------------")
        from connector import CloudDFSConnector, Error, NotFoundError, UnknownError, UnprocessableError

        for _ in range(1):
            conn = CloudDFSConnector('127.0.0.1', 9602)

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

    def test_data_group(self):
        """Test features only related in DataGroup.
        """
        print("----------------- test_data_group ----------------")
        from connector import CloudDFSConnector, Error, NotFoundError, UnknownError, UnprocessableError

        for _ in range(1):
            conn = CloudDFSConnector('127.0.0.1', 9602)

            group_names = [
                "Data Group Name #1",
                "Data Group Name #2",
                "Data Group Name #3",
            ]
            group_tokens = []

            def test_data_group(no: int):
                token = conn.create_data_group(group_names[no])
                group_tokens.append(token)
                info = conn.get_data_group_info(group_tokens[no])
                print("Information of Group #{0} : {1}".format(no, info))
                self.assertEqual(info['name'], group_names[no])

            test_data_group(0)
            conn.remove_data_group(group_tokens[0])
            try:
                conn.remove_data_group(group_tokens[0])
            except NotFoundError:
                pass
            else:
                self.assertTrue(False)
            test_data_group(1)
            conn.remove_data_group(group_tokens[1])
            test_data_group(2)
            conn.remove_data_group(group_tokens[2])

    def test_all(self):
        """Test all features.
        """
        print("----------------- test_all ----------------")
        from connector import CloudDFSConnector, Error, NotFoundError, UnknownError, UnprocessableError

        conn = CloudDFSConnector('127.0.0.1', 9602)

        file_names = [
            'Test File #1', 'Test File #2', 'Test File #3'
        ]
        file_data = [
            b'Test Data #1', 'Test Data #2', b'Test Data #3'
        ]
        data_types = [
            'binary', 'text', 'binary'
        ]
        data_tokens = []

        group_names = [
            "Data Group Name #1",
            "Data Group Name #2",
        ]
        group_tokens = []

        def check_data_file_remove(no):
            try:
                conn.get_data_file(data_tokens[no])
            except NotFoundError:
                pass
            else:
                self.assertTrue(False)

        def check_data_group_remove(no):
            try:
                conn.remove_data_group(group_tokens[no])
            except NotFoundError:
                pass
            else:
                self.assertTrue(False)

        group_tokens.append(conn.create_data_group(group_names[0]))
        group_tokens.append(conn.create_data_group(group_names[1]))

        data_tokens.append(conn.put_data_file(file_names[0], file_data[0], data_types[0], group_tokens[0]))
        data_tokens.append(conn.put_data_file(file_names[1], file_data[1], data_types[1], group_tokens[1]))
        data_tokens.append(conn.put_data_file(file_names[2], file_data[2], data_types[2], group_tokens[1]))

        self.assertEqual(conn.get_data_group_info(group_tokens[0]), {
            'name': group_names[0],
            'data_token_list': [data_tokens[0]]
        })
        self.assertEqual(conn.get_data_group_info(group_tokens[1]), {
            'name': group_names[1],
            'data_token_list': [data_tokens[1], data_tokens[2]]
        })

        conn.del_data_file(data_tokens[0])
        self.assertEqual(conn.get_data_group_info(group_tokens[0]), {
            'name': group_names[0],
            'data_token_list': []
        })
        check_data_file_remove(0)

        conn.remove_data_group(group_tokens[1])
        check_data_file_remove(1)
        check_data_file_remove(2)
        check_data_group_remove(1)

        conn.remove_data_group(group_tokens[0])
        check_data_group_remove(0)


if __name__ == '__main__':
    unittest.main()
