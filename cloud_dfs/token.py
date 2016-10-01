import random
from cloud_dfs.library import SingletonMeta


class Error(Exception):
    pass

class NotAvailableTokenError(Error):
    pass


def _generate_random_token(bytes_size: int = 512 // 8):
    return bytes(random.getrandbits(8) for _ in range(bytes_size))


class TokenManager(metaclass=SingletonMeta):
    MAX_GENERATE_TRYING_CNT = 100

    def __init__(self, allocated_tokens = None, f_gen_token = _generate_random_token):
        allocated_tokens = allocated_tokens if allocated_tokens else ()
        self._allocated_tokens = set(allocated_tokens)
        self._f_gen_token = f_gen_token
        print("Token Manager is initialized with", self._allocated_tokens, ', len :', len(self._allocated_tokens))

    def get_avail_token(self):
        trying_cnt = 1
        token = self._f_gen_token()
        avail = not token in self._allocated_tokens
        while trying_cnt <= self.MAX_GENERATE_TRYING_CNT and not avail:
            token = self._f_gen_token()
            avail = not token in self._allocated_tokens
            trying_cnt += 1

        if not avail:
            raise NotAvailableTokenError

        self._allocated_tokens.add(token)
        return token

    def del_token(self, token):
        self._allocated_tokens.remove(token)
