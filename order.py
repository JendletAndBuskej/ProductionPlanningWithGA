import random
from ponton import Ponton

class Order:
    def __init__(self, order_id, pontons, sign_date, due_date, prio_lvl):
        self.order_id = order_id
        self.pontons = pontons
        self.sign_date = sign_date
        self.due_date = due_date
        self.prio_lvl = prio_lvl
        self.set_order_in_pontons()

    def set_order_in_pontons(self):
        for ponton in self.pontons:
            ponton.order = self

    def print_stats(self):
        print(f"Order_{self.order_id}:")
        print(f" - order_id: {self.order_id}")
        print(f" - number_of_pontons: {len(self.pontons)}")
        print(f" - sign_date: {self.sign_date} [yyyy-mm-dd]")
        print(f" - due_date: {self.due_date} [yyyy-mm-dd]")
        print(f" - prio_lvl: {self.prio_lvl}")
