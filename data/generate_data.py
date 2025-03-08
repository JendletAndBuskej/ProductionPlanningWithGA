### Imports ###
# region
import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta
import yaml
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ponton import Ponton
from order import Order
# endregion


### Global varables ###
# region
number_of_pontoner = 30
number_of_orders = 7
number_of_locked_pontoner = 1   #if wants to be randomized
number_of_bedds = 5
hours_of_day = [6,18]
# endregion


### Help functions ###
# region
def aproximate_date(date_time):
    hour = date_time.hour
    closest_hour = hours_of_day[0] if hour < hours_of_day[1]-hours_of_day[0] else hours_of_day[1]
    date = date_time.replace(hour=closest_hour, minute=0, second=0, microsecond=0)
    return(date)

    # this is for the order specific values
def gernerate_rand_prio_lvl():
    PRIO_INTERVALL = [0,100]
    prio = round(random.uniform(PRIO_INTERVALL[0],PRIO_INTERVALL[1]),1)
    return (prio)

def generate_start_date():
    return(scedule_start_date)

def generate_due_date():
    return(scedule_start_date)

    # this is for locked specific values
def generate_pos():
    return([0,0])

def generate_bedd_id():
    rand_bedd = random.randint(1, number_of_bedds)
    return(rand_bedd)

def generate_time():
    start_date = scedule_start_date
    # Define the time range (0 days to 28 days ahead)
    random_days = random.randint(0, 28)
    random_seconds = random.randint(0, 24 * 60 * 60 - 1)  # Random time in a day
    # Calculate the final random date and time
    random_datetime = start_date + timedelta(days=random_days, seconds=random_seconds)
    random_datetime = aproximate_date(random_datetime)
    return(random_datetime)
# endregion


### Main Generation ###
# region
now = datetime.today()
scedule_start_date = aproximate_date(now)
    #pontons
order_splits = sorted(random.sample(range(2, number_of_pontoner+1), number_of_orders-1))
running_id = 0
running_order_id = 0
ponton_list = []
order_pontons = []
for iPonton in range(number_of_pontoner):
    running_id += 1
    if iPonton in order_splits or iPonton == 0:
        if iPonton != 0:
            order_obj = Order(running_order_id, order_pontons, sign_date, due_date, prio)
            order_pontons = []
        running_order_id += 1
        prio = gernerate_rand_prio_lvl()
        sign_date = generate_start_date()
        due_date = generate_due_date()
    ponton_obj = Ponton(id=running_id)
    ponton_list.append(ponton_obj)
    order_pontons.append(ponton_obj)
order_obj = Order(running_order_id, order_pontons, sign_date, due_date, prio)

    #locked pontons
running_order_id += 1
locked_ponton_list = []
prio = gernerate_rand_prio_lvl()
sign_date = generate_start_date()
due_date = generate_due_date()
for iLocked in range(number_of_locked_pontoner):
    running_id += 1
    pos = generate_pos()
    bedd_id = generate_bedd_id()
    time = generate_time()
    ponton_obj = Ponton(id=running_id, is_locked=True, 
                        pos=pos, bedd_id=bedd_id, time=time)
    locked_ponton_list.append(ponton_obj)
order_obj = Order(running_order_id, locked_ponton_list, sign_date, due_date, prio)
# endregion


### Save yaml ###
# region
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True  # Prevents YAML from using anchors and aliases

def save_ponton_data_to_yaml(ponton_list, locked_ponton_list, planned_start_date, filename="data/pontons.yaml"):
    # Process unlocked pontoner
    pontoner_data = []
    for ponton_obj in ponton_list:
        ponton_dict = ponton_obj.get_dict()
        ponton_dict["sign_date"] = str(ponton_dict["sign_date"])
        ponton_dict["due_date"] = str(ponton_dict["due_date"])
        pontoner_data.append(ponton_dict)
    # Process locked pontoner
    locked_pontoner_data = []
    for ponton_obj in locked_ponton_list:
        ponton_dict = ponton_obj.get_dict()
        ponton_dict["sign_date"] = str(ponton_dict["sign_date"])
        ponton_dict["due_date"] = str(ponton_dict["due_date"])
        locked_pontoner_data.append(ponton_dict)
    # Create final structured data
    yaml_data = {
        "planned_start_date": str(planned_start_date),
        "pontoner": pontoner_data,
        "locked_pontoner": locked_pontoner_data
    }
    # Write to YAML file
    with open(filename, "w") as file:
        yaml.dump(yaml_data, file, default_flow_style=False, allow_unicode=True, sort_keys=False, Dumper=NoAliasDumper)

save_ponton_data_to_yaml(ponton_list, locked_ponton_list, scedule_start_date)
# endregion


