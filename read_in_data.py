import yaml
from ponton import Ponton
from order import Order

def load_orders_from_yaml(filename):
    """ Reads a YAML file and returns the planned_start_date, list of Order objects & list of locked Ponton objects. """

    with open(filename, "r") as file:
        data = yaml.safe_load(file)  # Load YAML data

    planned_start_date = data["planned_start_date"]  # Extract planned start date

    ponton_objects = {}  # Dictionary to store ponton_id -> Ponton object
    order_objects = {}   # Dictionary to store order_id -> Order object
    locked_pontons = []  # List for locked pontons

    # Process unlocked pontons
    for ponton_data in data["pontoner"]:
        ponton_obj = Ponton(
            id=ponton_data["id"],
            size=ponton_data["size"],
            cure_time=ponton_data["cure_time"],
            team_size=ponton_data["team_size"]
        )
        ponton_objects[ponton_data["id"]] = ponton_obj  # Store ponton object

        order_id = ponton_data["order_id"]
        if order_id not in order_objects:
            order_objects[order_id] = Order(
                order_id=order_id,
                pontons=[],
                sign_date=ponton_data["sign_date"],
                due_date=ponton_data["due_date"],
                prio_lvl=ponton_data["prio_lvl"]
            )

        order_objects[order_id].pontons.append(ponton_obj)  # Assign ponton to its order

    # Process locked pontons
    for ponton_data in data["locked_pontoner"]:
        ponton_obj = Ponton(
            id=ponton_data["id"],
            size=ponton_data["size"],
            cure_time=ponton_data["cure_time"],
            team_size=ponton_data["team_size"],
            is_locked=True,
            pos=ponton_data["pos"],
            bedd_id=ponton_data["bedd_id"],
            time=ponton_data["time"]
        )
        ponton_objects[ponton_data["id"]] = ponton_obj  # Store ponton object
        locked_pontons.append(ponton_obj)  # Add to locked list

        order_id = ponton_data["order_id"]
        if order_id not in order_objects:
            order_objects[order_id] = Order(
                order_id=order_id,
                pontons=[],
                sign_date=ponton_data["sign_date"],
                due_date=ponton_data["due_date"],
                prio_lvl=ponton_data["prio_lvl"]
            )

        order_objects[order_id].pontons.append(ponton_obj)  # Assign locked ponton to its order

    # Convert dictionary values to list
    order_list = list(order_objects.values())
    print(f"Loaded {len(order_list)} orders and {len(locked_pontons)} locked pontons.")
    return planned_start_date, order_list, locked_pontons  # Return planned start date, orders, and locked pontons
