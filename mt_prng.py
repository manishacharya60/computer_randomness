class MersenneTwister:
    def __init__(self, seed=5489):
        self.n = 624  # State size
        self.mt = [0] * self.n  # State vector
        self.index = self.n
        self.lower_mask = (1 << 31) - 1  # Lower 31 bits
        self.upper_mask = 1 << 31  # Upper bit

        # Initialize state
        self.mt[0] = seed
        for i in range(1, self.n):
            self.mt[i] = (1812433253 * (self.mt[i-1] ^ (self.mt[i-1] >> 30)) + i) & 0xFFFFFFFF

    def twist(self):
        for i in range(self.n):
            x = (self.mt[i] & self.upper_mask) + (self.mt[(i+1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA ^= 0x9908B0DF 
            self.mt[i] = self.mt[(i + 397) % self.n] ^ xA
        self.index = 0

    def next(self):
        if self.index >= self.n:
            self.twist()

        y = self.mt[self.index]
        self.index += 1

        # Tempering transformations
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= (y >> 18)

        return y & 0xFFFFFFFF

seed = int(input("Enter an initial seed: "))

listPrngs = MersenneTwister(seed)
print([listPrngs.next() for _ in range(10)])
