import math

class Point:

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def show(self):
        print(f"({self.x}, {self.y})")

    def move(self,x,y):
        self.x=x
        self.y=y

    def dist(self,other):
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2)


x1,y1=map(int,input().split())
x2,y2=map(int,input().split())
x3,y3=map(int,input().split())

p=Point(x1,y1)
p.show()

p.move(x2,y2)
p.show()

p2=Point(x3,y3)

print(f"{p.dist(p2):.2f}")
