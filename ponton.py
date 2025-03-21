### Ponton Class ###
import random

class Ponton:
    def __init__(self, id, size=[None,None], cure_time=None, 
                 team_size=None, is_locked=False, pos=[None,None], bedd_id=None, time=None):
        self.id = id
        self.order = None
        if size[0] is None:
            self.size = self.generate_rand_size()
        else:
            self.size = size    #[meter,meter]
        if cure_time is None:
            self.cure_time = self.gernerate_rand_cure_time(self.size)
        else:
            self.cure_time = cure_time #days
        if team_size is None:
            self.team_size = self.gernerate_rand_team_size(self.size)
        else:
            self.team_size = team_size
        self.is_locked = is_locked
        self.pos = pos
        self.bedd_id = bedd_id
        self.time = time
        if self.is_locked:
            if not self.pos:
                print(f"[ERROR]: locked ponton_{self.id} is missing pos")
            if not self.bedd_id:
                print(f"[ERROR]: locked ponton_{self.id} is missing bedd_id")
            if not self.time:
                print(f"[ERROR]: locked ponton_{self.id} is missing time")
        pass

    def generate_rand_size(self):
        ''' will make sure that height is larger than width
        '''
        MIN_SIZE = [2,8]
        MAX_SIZE = [10,30]
        self.MIN_SIZE = MIN_SIZE
        self.MAX_SIZE = MAX_SIZE
        width = round(random.uniform(MIN_SIZE[0],MAX_SIZE[0]),1)
        height = round(random.uniform(max(width,MIN_SIZE[1]),MAX_SIZE[1]),1)
        return ([width, height])
    
    def gernerate_rand_cure_time(self, size):
        '''This will give a larger cure time with larger size with a small deviation
        '''
        def normalize(num, a, b):
            return (num - a) / (b - a)
        CURE_TIME_INTERVALL = [7,21]
        MAX_DEVIATION = 0.2
        normalized_width = normalize(size[0], self.MIN_SIZE[0], self.MAX_SIZE[0])
        normalized_height = normalize(size[1], self.MIN_SIZE[1], self.MAX_SIZE[1])
        normalized_area = normalized_width*normalized_height
        deviated_area = normalized_area + random.uniform(-MAX_DEVIATION, MAX_DEVIATION)
        deviated_norm_area = max(0, min(1, deviated_area))
        cure_time = CURE_TIME_INTERVALL[0] + deviated_norm_area*(CURE_TIME_INTERVALL[1]-CURE_TIME_INTERVALL[0])
        cure_time = round(cure_time)
        return (cure_time)
    
    def gernerate_rand_team_size(self, size):
        def normalize(num, a, b):
            return (num - a) / (b - a)
        TEAM_SIZE_INTERVALL = [3,6]
        MAX_DEVIATION = 0.33
        normalized_width = normalize(size[0], self.MIN_SIZE[0], self.MAX_SIZE[0])
        normalized_height = normalize(size[1], self.MIN_SIZE[1], self.MAX_SIZE[1])
        normalized_area = normalized_width*normalized_height
        deviated_area = normalized_area + random.uniform(-MAX_DEVIATION, MAX_DEVIATION)
        deviated_norm_area = max(0, min(1, deviated_area))
        team_size = TEAM_SIZE_INTERVALL[0] + deviated_norm_area*(TEAM_SIZE_INTERVALL[1]-TEAM_SIZE_INTERVALL[0])
        team_size = round(team_size)
        return (team_size)
    
    def place(self, bedd, pos, time):
        self.bedd = bedd
        self.pos = pos
        self.time = time
        pass

    def print_stats(self):
        print(f"Ponton_{self.id}:")
        print(f" - id: {self.id}")
        print(f" - order_id: {self.order.order_id}")
        print(f" - size: {self.size} [m]")
        # print(f" - sign_date: {self.order.sign_date}")
        # print(f" - due_date: {self.order.due_date}")
        # print(f" - prio_lvl: {self.order.prio_lvl}")
        print(f" - cure_time: {self.cure_time} [days]")
        print(f" - team_size: {self.team_size} [people]")
        print(f" - is_locked: {self.is_locked}")
        if self.is_locked or self.pos:
            print(f"   -- bedd_id: {self.bedd_id}")
            print(f"   -- pos: {self.pos} [m]")
            print(f"   -- time: {self.time}")
        else:
            print("   -- is not sceduled with bedd, pos and time")
        pass

    def get_dict(self):
        if self.is_locked or self.pos:
            ponton_dict = {
            "id": self.id,
            "order_id": self.order.order_id,
            "size": self.size,
            "sign_date": str(self.order.sign_date),
            "due_date": str(self.order.due_date),
            "prio_lvl": self.order.prio_lvl,
            "cure_time": self.cure_time,
            "team_size": self.team_size,
            "pos": self.pos,
            "bedd_id": self.bedd_id,
            "time": self.time
        }
        else:
            ponton_dict = {
            "id": self.id,
            "order_id": self.order.order_id,
            "size": self.size,
            "sign_date": str(self.order.sign_date),
            "due_date": str(self.order.due_date),
            "prio_lvl": self.order.prio_lvl,
            "cure_time": self.cure_time,
            "team_size": self.team_size
        }
        return(ponton_dict)

