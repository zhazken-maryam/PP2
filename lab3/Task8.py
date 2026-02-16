class Account:

    def __init__(self,balance):
        self.balance=balance

    def withdraw(self,amount):

        if amount>self.balance:
            print("Insufficient Funds")
        else:
            self.balance-=amount
            print(self.balance)


b,w=map(int,input().split())

acc=Account(b)

acc.withdraw(w)
