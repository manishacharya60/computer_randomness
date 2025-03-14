# m=9 c=7 a=4

class LCGPrng:
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32-1):
        self.state = seed
        self.a = a
        self.c = c
        self.m = m
    
    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

seed = int(input("Enter an initial seed: "))

listPrngs = LCGPrng(seed)
print([listPrngs.next() for _ in range(10)])
