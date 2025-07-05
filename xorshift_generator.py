# XORShift Generator implementation using bitwise operations.

class XORShiftGenerator:
    def __init__(self, seed=12345):
        """
        Initialize XORShift generator with seed.
        
        Args:
            seed: Initial seed value (must be non-zero)
        """
        if seed == 0:
            raise ValueError("Seed cannot be zero for XORShift generator")
        self.seed = seed
        self.state = seed
    
    def next(self):
        # Generate next random number using XORShift algorithm.
        self.state ^= self.state << 13
        self.state ^= self.state >> 17
        self.state ^= self.state << 5
        
        # Ensure state stays within 32-bit range
        self.state &= 0xFFFFFFFF
        
        return self.state
    
    def generate_sequence(self, n):
        # Generate sequence of n random numbers.
        return [self.next() for _ in range(n)]
    
    def reset(self, seed=None):
        # Reset generator to initial or new seed.
        if seed is not None:
            if seed == 0:
                raise ValueError("Seed cannot be zero for XORShift generator")
            self.seed = seed
        self.state = self.seed
    
    def normalized_next(self):
        # Generate normalized random number between 0 and 1.
        return self.next() / 0xFFFFFFFF
    
    def normalized_sequence(self, n):
        # Generate sequence of n normalized random numbers.
        return [self.normalized_next() for _ in range(n)]