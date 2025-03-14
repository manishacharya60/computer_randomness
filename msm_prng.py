class MSMPrng:
    def __init__(self, seed, digit):
        self.state = seed
        self.digit = digit
    
    def next(self):
        self.state = self.state ** 2
        seedStr = str(self.state).zfill(2*self.digit)
        midIndex = (len(seedStr) - self.digit) // 2
        self.state = int(seedStr[midIndex:midIndex+self.digit])
        return self.state

seed = int(input("Enter an initial seed: "))
digit = int(input("Enter the number of digits: "))

if (len(str(seed)) < digit):
    print("Seed must have at least as many digits as 'digit'.")
else:
    listPrngs = MSMPrng(seed, digit)
    print([listPrngs.next() for _ in range(10)])