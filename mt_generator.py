# Mersenne Twister PRNG implementation using Python's random module

import random

class MTGenerator:
    def __init__(self, seed=None):
        """
        Initialize Mersenne Twister generator with optional seed.
        
        Args:
            seed: Initial seed value (None for system time)
        """
        self.rng = random.Random()
        if seed is not None:
            self.rng.seed(seed)
        self.initial_seed = seed
    
    def next(self):
        # Generate next random integer.
        return self.rng.getrandbits(32)
    
    def generate_sequence(self, n):
        # Generate sequence of n random integers.
        return [self.next() for _ in range(n)]
    
    def reset(self, seed=None):
        # Reset generator to initial or new seed.
        if seed is not None:
            self.initial_seed = seed
        self.rng.seed(self.initial_seed)
    
    def normalized_next(self):
        # Generate normalized random number between 0 and 1.
        return self.rng.random()
    
    def normalized_sequence(self, n):
        # Generate sequence of n normalized random numbers.
        return [self.normalized_next() for _ in range(n)]
    
    def randint(self, a, b):
        # Generate random integer in range [a, b].
        return self.rng.randint(a, b)
    
    def uniform(self, a, b):
        # Generate uniform random float in range [a, b].
        return self.rng.uniform(a, b)