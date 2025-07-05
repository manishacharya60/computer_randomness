# Cryptographically Secure PRNG (CSPRNG) implementation using Python's secrets module

import secrets
import os

class CSPRNGGenerator:
    def __init__(self, seed=None):
        # seed: Not used for CSPRNG (cryptographically secure generators don't use seeds)
        pass
    
    def next(self):
        # Generate next cryptographically secure random integer.
        return secrets.randbits(32)
    
    def generate_sequence(self, n):
        # Generate sequence of n cryptographically secure random integers.
        return [self.next() for _ in range(n)]
    
    def reset(self, seed=None):
        # Reset is not applicable for CSPRNG as it uses system entropy.
        pass
    
    def normalized_next(self):
        # Generate normalized cryptographically secure random number between 0 and 1.
        return secrets.randbits(32) / (2**32)
    
    def normalized_sequence(self, n):
        # Generate sequence of n normalized cryptographically secure random numbers.
        return [self.normalized_next() for _ in range(n)]
    
    def randbelow(self, n):
        # Generate cryptographically secure random integer below n.
        return secrets.randbelow(n)
    
    def token_bytes(self, nbytes):
        # Generate cryptographically secure random bytes.
        return secrets.token_bytes(nbytes)
    
    def token_hex(self, nbytes):
        # Generate cryptographically secure random hex string.
        return secrets.token_hex(nbytes)
    
    def system_random(self):
        # Generate random number using system entropy directly.
        return int.from_bytes(os.urandom(4), 'big') / (2**32)