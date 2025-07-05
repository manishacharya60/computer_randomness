# Linear Congruential Generator (LCG) implementation.
# Formula: X_{n+1} = (a * X_n + c) mod m

class LCGGenerator:
    def __init__(self, seed=1, modulus=2**31 - 1, multiplier=1664525, increment=1013904223):
        """
        Initialize LCG with configurable parameters.
        
        Args:
            seed: Initial seed value
            modulus: Modulus value (m)
            multiplier: Multiplier value (a)
            increment: Increment value (c)
        """
        self.seed = seed
        self.modulus = modulus
        self.multiplier = multiplier
        self.increment = increment
        self.current = seed
    
    def next(self):
        # Generate next random number.
        self.current = (self.multiplier * self.current + self.increment) % self.modulus
        return self.current
    
    def generate_sequence(self, n):
        # Generate sequence of n random numbers.
        return [self.next() for _ in range(n)]
    
    def reset(self, seed=None):
        # Reset generator to initial or new seed.
        if seed is not None:
            self.seed = seed
        self.current = self.seed
    
    def normalized_next(self):
        # Generate normalized random number between 0 and 1.
        return self.next() / self.modulus
    
    def normalized_sequence(self, n):
        # Generate sequence of n normalized random numbers.
        return [self.normalized_next() for _ in range(n)]