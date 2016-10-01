import unittest


class MyTestCase(unittest.TestCase):

    def test_database(self):

        from cloud_dfs.database import init_db
        from cloud_dfs.database import db_session
        from cloud_dfs.database.models import Data
        from cloud_dfs.token import TokenManager

        init_db()
        data_obj_list = db_session.query(Data).all()
        allocated_tokens = [data_obj.token for data_obj in data_obj_list]
        token_manager = TokenManager(allocated_tokens)

        data = Data('test_data', token_manager.get_avail_token(), 'test_path')
        db_session.add(data)
        db_session.commit()


if __name__ == '__main__':
    unittest.main()
