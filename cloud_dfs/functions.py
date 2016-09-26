import random


def generate_random_token(bytes_size: int = 512 // 8):
    return bytes(random.getrandbits(8) for _ in range(bytes_size))