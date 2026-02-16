# This class represents a pair of numbers
class Pair:

    def __init__(self, a, b):
        self.a = a   # store first value
        self.b = b   # store second value

    def add(self, other):
        # return a new Pair with summed values
        return Pair(self.a + other.a, self.b + other.b)


# get four integers from user input
a1, b1, a2, b2 = map(int, input().split())

# create first Pair object
p1 = Pair(a1, b1)

# create second Pair object
p2 = Pair(a2, b2)

# add the two Pair objects
res = p1.add(p2)

# print the result
print(f"Result: {res.a} {res.b}")

