"""This file contains the Budget class to instantiate Budget objects for later use"""


class budget:

    def __init__(self, date, amount):
        self.date = date
        self.amount = amount

    def view_budget(self):
        print("budget received at : ", self.date, " Amount : ", self.amount)
