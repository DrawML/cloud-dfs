import unittest


class MyTestCase(unittest.TestCase):

    def test_database(self):

        from cloud_dfs.database import init_db
        from cloud_dfs.database import db_session
        from cloud_dfs.database.models import Data
        from cloud_dfs.library import generate_random_token

        init_db()

        data = Data('test_data', generate_random_token(), 'test_path')
        db_session.add(data)
        db_session.commit()


if __name__ == '__main__':
    unittest.main()
