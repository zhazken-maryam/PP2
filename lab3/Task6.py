class Shape:
    def area(self):
        return 0

class Rectangle(Shape):

    def __init__(self,l,w):
        self.l=l
        self.w=w

    def area(self):
        return self.l*self.w


l,w=map(int,input().split())

r=Rectangle(l,w)

print(r.area())
