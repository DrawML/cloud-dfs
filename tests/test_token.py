import unittest
from cloud_dfs.token import TokenManager, NotAvailableTokenError

class MyTestCase(unittest.TestCase):

    def test_token(self):

        class TokenGeneratorForTest(object):

            def __init__(self):
                self.no = 0

            def __call__(self, *args, **kwargs):
                self.no += 1
                return self.no

        token_manager = TokenManager([1,3,4,6,9,11,12,13], TokenGeneratorForTest())

        self.assertEqual(token_manager.get_avail_token(), 2)
        self.assertEqual(token_manager.get_avail_token(), 5)
        self.assertEqual(token_manager.get_avail_token(), 7)
        self.assertEqual(token_manager.get_avail_token(), 8)
        self.assertEqual(token_manager.get_avail_token(), 10)
        token_manager.del_token(11)
        token_manager.del_token(13)
        self.assertEqual(token_manager.get_avail_token(), 11)
        self.assertEqual(token_manager.get_avail_token(), 13)


if __name__ == '__main__':
    unittest.main()
