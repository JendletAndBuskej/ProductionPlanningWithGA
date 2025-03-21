import numpy as np 
from gen import Gen
import copy
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
        for iIndividual in range(self.population_count):
            gen = Gen(
                self.orders, self.beds, self.bed_nbr_slots_x,
                self.bed_nbr_slots_x, self.nbr_time_slots
            )
            # extract data from initial schedule and mak
            gen.randomize_gen()
            self.population[iIndividual] = gen
            print(f"Indi {iIndividual} has value {gen.fitness_score()}")
        self.find_and_set_fittest_individual()
        self.genomes_per_gen = np.shape(self.population[0].gen)[0]
        return self
    
    def mutate(self, gen: Gen):
        gen_length = np.shape(gen.gen)[0]
        mutation_rate = self.mutation_multiplier/float(gen_length)
        for genome in gen.gen:
            r = np.random.uniform(0, 1)
            if r > mutation_rate:
                continue
            genome = 1 if genome == 0 else 0
        return gen
    
    def find_and_set_fittest_individual(self):
        fittest_value = -1000
        if self.fittest_individual:
            fittest_value = self.fittest_individual.fitness_score()
        for individual in (self.population):
            if individual.fitness_score() > fittest_value:
                self.fittest_individual = copy.deepcopy(individual)
        return self

    def accumulated_norm_fitness(self):
        all_fitness_values = [individual.fitness_score() for individual in (self.population)]
        total_fitness = sum(all_fitness_values)
        cum_fitness = 0
        accum_norm_fitness = np.empty([0,],dtype=float)
        for individual in (self.population):
            individual_norm_fitness = individual.fitness_score()/total_fitness
            cum_fitness += individual_norm_fitness
            accum_norm_fitness = np.append(accum_norm_fitness,cum_fitness)
        return accum_norm_fitness
    
    def roulette_wheel_selection(self):
        # other methods can be found on https://en.wikipedia.org/wiki/Selection_(evolutionary_algorithm)
        # example being Rank Selection, Stochastic universal sampling, Steady state, truncation, elitist, boltzmann, tournament
        accumulated_norm_fitness = self.accumulated_norm_fitness()
        selections = np.empty([self.population_count,1],dtype=object)
        for iSelection in range(self.population_count):
            random_selection_value = np.random.uniform(0,1)
            for iIndividual, individual in enumerate(self.population):
                if accumulated_norm_fitness[iIndividual] < random_selection_value:
                    continue
                # selections[iSelection,0] = copy.deepcopy(individual)
                selections[iSelection,0] = copy.deepcopy(individual)
                break
        selection_pairs = np.empty([self.population_count//2,2],dtype=object)
        selection_pairs[:,0] = selections[:self.population_count//2,0]
        selection_pairs[:,1] = selections[self.population_count//2:,0]
        return selection_pairs

    def crossover_uniform(self, gen_father: Gen, gen_mother: Gen):
        gen_son = copy.deepcopy(gen_father)
        gen_daughter = copy.deepcopy(gen_mother)
        for iGenome in range(self.genomes_per_gen):
            r = np.random.uniform(0, 1)
            if r > .5:
                genome_son = gen_son.gen[iGenome]
                gen_son.gen[iGenome] = gen_daughter.gen[iGenome]
                gen_daughter.gen[iGenome] = genome_son
        return gen_son, gen_daughter
    
    def crossover_k_point(self, gen_father: Gen, gen_mother: Gen, k_points: int):
        gen_son = copy.deepcopy(gen_father)
        gen_daughter = copy.deepcopy(gen_mother)
        random_points = np.random.choice(np.arange(1, self.genomes_per_gen - 1), size=k_points, replace=False)
        points = np.sort(random_points)
        print(points)
        for iPoint, point in enumerate(points):
            gen_son.gen[point:] = gen_mother.gen[point:]
            gen_daughter.gen[point:] = gen_father.gen[point:]
            if iPoint % 2 == 1:
                gen_son.gen[point:] = gen_father.gen[point:]
                gen_daughter.gen[point:] = gen_mother.gen[point:]
        return gen_son, gen_daughter
        
    def do_generation(self):
        if not self.population.all():
            # log?
            return
        selection_pairs = self.roulette_wheel_selection()
        new_population = np.empty([self.population_count,],dtype=object)
        for iPair, selection_pair in enumerate(selection_pairs):
            print("iPair: ",iPair)
            father_gen = selection_pair[0]
            mother_gen = selection_pair[1]
            gen_son, gen_daughter = self.crossover_k_point(father_gen,mother_gen,k_points=3)
            # gen_son = self.mutate(gen_son)
            # gen_daughter = self.mutate(gen_daughter)
            new_population[2*iPair] = gen_son
            new_population[2*iPair+1] = gen_daughter
        self.population = new_population
        self.find_and_set_fittest_individual()
        return self
    
# GA = GeneticAlgorithm([3,2],[1,2],2,2,3,100)
# # GA.generate_population().crossover_uniform(GA.population[0],GA.population[1])
# # GA = GA.generate_population().crossover_k_point(GA.population[0],GA.population[1],3).roulette_wheel_selection()
# GA = GA.generate_population()
# for i in range(500):
#     GA.do_generation()
#     # print(GA.fittest_individual.fitness_score())
# print(GA.fittest_individual.fitness_score())
# for genome in GA.fittest_individual.gen:
#     print(genome)

# Start of a test
GA = GeneticAlgorithm(
    orders=[3,2],beds=[1,2],
    bed_nbr_slots_x=2,
    bed_nbr_slots_y=2,
    nbr_time_slots=3,
    population_count=2
    )
GA.generate_population()

gen1 = Gen(
    orders=[3,2],beds=[1,2],
    bed_nbr_slots_x=2,
    bed_nbr_slots_y=2,
    nbr_time_slots=3)
gen2 = Gen(
    orders=[3,2],beds=[1,2],
    bed_nbr_slots_x=2,
    bed_nbr_slots_y=2,
    nbr_time_slots=3,test=1)
GA.population[0] = gen1
GA.population[1] = gen2

print(GA.population[0].gen)
print(GA.population[1].gen)