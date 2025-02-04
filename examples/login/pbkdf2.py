import os
import hashlib

# PBKDF2 secure password hashing algorithm obtained from:
# https://codeandlife.com/2023/01/06/how-to-calculate-pbkdf2-hmac-sha256-with-
# python,-example-code/


def sha256(b):
    return hashlib.sha256(b).digest()


def ljust(b, n, f):
    return b + f * (n - len(b))


def gethmac(key, content):
    okeypad = bytes(v ^ 0x5c for v in ljust(key, 64, b'\0'))
    ikeypad = bytes(v ^ 0x36 for v in ljust(key, 64, b'\0'))
    return sha256(okeypad + sha256(ikeypad + content))


def pbkdf2(pwd, salt, iterations=1000):
    U = salt + b'\x00\x00\x00\x01'
    T = bytes(64)
    for _ in range(iterations):
        U = gethmac(pwd, U)
        T = bytes(a ^ b for a, b in zip(U, T))
    return T


# The number of iterations may need to be adjusted depending on the hardware.
# Lower numbers make the password hashing algorithm faster but less secure, so
# the largest number that can be tolerated should be used.
def generate_password_hash(password, salt=None, iterations=100000):
    salt = salt or os.urandom(16)
    dk = pbkdf2(password.encode(), salt, iterations)
    return f'pbkdf2-hmac-sha256:{salt.hex()}:{iterations}:{dk.hex()}'


def check_password_hash(password_hash, password):
    algorithm, salt, iterations, dk = password_hash.split(':')
    iterations = int(iterations)
    if algorithm != 'pbkdf2-hmac-sha256':
        return False
    return pbkdf2(password.encode(), salt=bytes.fromhex(salt),
                  iterations=iterations) == bytes.fromhex(dk)
