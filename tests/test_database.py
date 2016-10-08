import unittest


class MyTestCase(unittest.TestCase):

    def test_database(self):

        from cloud_dfs.database import init_db
        from cloud_dfs.database import db_session
        from cloud_dfs.database.models import Data, DataGroup
        from cloud_dfs.token import TokenManager
        import sqlalchemy

        init_db()
        data_obj_list = db_session.query(Data).all()
        allocated_tokens = [data_obj.token for data_obj in data_obj_list]
        token_manager = TokenManager(allocated_tokens)

        data_group = DataGroup('test_data_group', token_manager.get_avail_token())
        db_session.add(data_group)
        db_session.commit()

        data_group2 = DataGroup('test_data_group', token_manager.get_avail_token())
        db_session.add(data_group2)
        db_session.commit()

        data = Data('test_data', token_manager.get_avail_token(), 'test_path', 'text', data_group)
        db_session.add(data)
        db_session.commit()

        print(data_group.data_list)
        print(data_group2.data_list)
        print(data.data_group)
        print(data.fk_data_group)

        db_session.delete(data_group)
        db_session.commit()

        try:
            data = db_session.query(Data).filter(Data.token == data.token).one()
        except sqlalchemy.orm.exc.NoResultFound:
            pass
        else:
            self.assertTrue(False)

        data = db_session.query(DataGroup).filter(DataGroup.id == data_group2.id).delete()

        db_session.commit()


if __name__ == '__main__':
    unittest.main()
