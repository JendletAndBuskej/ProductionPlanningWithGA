import numpy as np 
from gen import Gen
# from order import Order
# from bed import Bed

class GeneticAlgorithm():
    def __init__(self,
            orders: list[int], beds: list[int], bed_nbr_slots_x: int, bed_nbr_slots_y: int,
            nbr_time_slots: int, population_count: int, mutation_multiplier: int=1.
        ):
        self.orders = orders
        self.beds = beds
        self.bed_nbr_slots_x = bed_nbr_slots_x
        self.bed_nbr_slots_y = bed_nbr_slots_y
        self.nbr_time_slots = nbr_time_slots
        self.population_count = population_count
        self.mutation_multiplier = mutation_multiplier
        self.fittest_individual = None
    
    def generate_population(self):
        self.population = np.empty([self.population_count,],dtype=object)
        for iGen in range(self.population_count):
            gen = Gen(
                self.orders, self.beds, self.bed_nbr_slots_x,
                self.bed_nbr_slots_x, self.nbr_time_slots
            )
            # extract data from initial schedule and mak
            gen.randomize_gen()
            self.population[iGen] = gen
    
    def mutate(self, gen: Gen):
        gen_length = np.shape(gen)[0]
        mutation_rate = self.mutation_multiplier/float(gen_length)
        for genome in gen:
            r = np.random.uniform(0, 1)
            if r > mutation_rate:
                continue
            genome = 1 if genome == 0 else 0
        return self
    
    def crossover(self, gen_father: Gen, gen_mother: Gen):
        pass
    def do_generation():
        pass

GA = GeneticAlgorithm([3,2],[1,2],2,2,3,60)
GA.generate_population()