#!/usr/bin/python3

class MersennePrimesLucasLehmer :
    # 2 ** p - 1 = m, p > 0
    power = 1
    mersenne = 1
    
    # N1 ** 2 - 2 = N2, start@4
    lucas_number = 4
    lucas_index = 1
    
    # Mersenne
    
    def get_power(self) :
        return self.power
    
    def set_power(self, x) :
        assert x >= 1, "Positive only."
        self.power = x
        self.mersenne = 2 ** x - 1
    
    def get_mersenne(self) :
        return self.mersenne
    
    def set_mersenne(self, x) :
        assert x > 3, "Positive 4-on only."
        y = bin(x)[2 :]
        assert all(z == '1' for z in y), "Of Mersenne only."
        self.mersenne = x
        self.power = len(y)
    
    # Lucas-Lehmer
    
    def lucas_get_step(self) :
        return self.lucas_index
    
    def lucas_advance1(self) :
        self.lucas_index += 1
        self.lucas_number = (self.lucas_number ** 2 - 2) % self.mersenne
    
    def lucas_reset(self) :
        self.lucas_number = 4
        self.lucas_index = 1
    
    # If N[p - 1] mod m is 0, m is prime.
    
    def is_prime(self) :
        assert self.get_power() - 1 == self.lucas_get_step(), "Premature operation."
        return not self.lucas_number


a = MersennePrimesLucasLehmer()

for x in range(2, 21) :
    a.set_power(x)
    for _ in range(x - 2) : a.lucas_advance1()
    print('True ' if a.is_prime() else 'False', bin(a.get_mersenne())[2 :].rjust(21, '0'), a.get_mersenne())
    a.lucas_reset()
