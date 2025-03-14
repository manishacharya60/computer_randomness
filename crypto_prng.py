import os
import secrets
import hashlib
from Crypto.Cipher import AES

class HashPrng:
    def __init__(self, seed):
        self.state = seed.to_bytes(32, 'big')  # Convert integer to bytes

    def next(self):
        # Apply SHA-256 hashing to generate new random state
        self.state = hashlib.sha256(self.state).digest()
        return int.from_bytes(self.state[:4], 'big')  # Convert first 4 bytes to integer

class AES_CSPRNG:
    def __init__(self, seed):
        self.key = os.urandom(16)  # 128-bit key
        self.counter = 0

    def next(self):
        cipher = AES.new(self.key, AES.MODE_ECB)
        counter_bytes = self.counter.to_bytes(16, 'big')
        self.counter += 1
        return int.from_bytes(cipher.encrypt(counter_bytes), 'big')

# Get user input for the seed
seed = int(input("Enter an initial seed: "))

# Secure randomness using Python's `secrets` module
secretNum = secrets.randbits(32)
print("Secure Random Number (32-bit) using 'secrets': ", secretNum)

# Secure randomness using system entropy (`os.urandom`)
systemNum = os.urandom(16)
print("Secure Random Bytes using system entropy: ", systemNum.hex())

# Secure randomness using SHA-256 hashing
csprng = HashPrng(seed=seed)
print("Secure Random Number using hashing (SHA-256): ", csprng.next()) 

# Secure randomness using AES-CTR PRNG
aes_prng = AES_CSPRNG(seed=seed)
print("Secure Random Number using AES-CTR: ", aes_prng.next())  
