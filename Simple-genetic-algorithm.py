#--------------------------------
#
#   Author: Idham (2019717453)
#
#-------------------------------

import random
import time

#can only do multiple of 2: starting 4,8,16,32,64 and so on because I use half deletion during selection
POP_SIZE = 8 
GENE_SIZE = 6 #chromosome length
MUTATION_RATE = 0.2
GENERATION_LIMIT = 1000
CROSSOVER_POINT = 1 # 1 or 2

class Individual:

    def __init__(self, chromosome, geneticinfo):
        self.chromosome = chromosome    #Exp: [0,0,0,0,0,0]
        self.geneticinfo = geneticinfo  #Exp: Gen0 - Chromosome #0
        self.x = 0                      #Value of chromosome
        self.fitness = 0                #Calculated Fitness

    def setChromosome(self, chromosome):
        self.chromosome = chromosome

    def setgeneticinfo(self, geneticstr):
        self.geneticinfo = geneticstr

    def setX(self, x):
        self.x = x

    def setFitness(self, fitvalue):
        self.fitness = fitvalue

#Chromosome Binary Array to Decimal
def chrotodec(chromosome):
    total = 0
    power = GENE_SIZE - 1
    for x in range(GENE_SIZE):
        total += chromosome[x]*2**power
        power -= 1
    return total

#Chromosome Binary Array to Decimal with f(x) = x^2
def chrotodecfit(chromosome):
    total = 0
    power = GENE_SIZE - 1
    for x in range(GENE_SIZE):
        total += chromosome[x]*2**power
        power -= 1
    return total**2

#sortPopulation based on fitness
def sortPopulation(individual):
    return individual.fitness

#initialize
def initialize(popsize):
    population = []
    for x in range(popsize):
        chromosome = []
        for y in range(GENE_SIZE):
            chromosome.append(random.randint(0, 1))
        population.append(Individual(chromosome, "Gen0 - Chromosome #"+str(x+1)))
    return population

#fitness calculation
def fitness_calc(population):
    for x in population:
        x.setX(chrotodec(x.chromosome))
        x.setFitness(chrotodecfit(x.chromosome))
        print(f"{x.geneticinfo} = X: {x.x}, fitness: {x.fitness}")

#selection
def selection(population):
    #select half of population, 3/4 from best fit and 1/4 worst fit
    halfpop = int(POP_SIZE/2)
    #delete half of population because of that only certain number of population is allow.
    #it is because i use 3/4 * half of population which cause selection did not select the correct amount of selected genetic
    bestfitselect = random.sample(population[0:halfpop-1], int((3/4)*halfpop))
    worstfitselect = random.sample(population[halfpop:POP_SIZE], int((1/4)*halfpop))
    survivepop = bestfitselect+worstfitselect
    return survivepop

#crossover
def crossover(population, gen):
    random.shuffle(population)
    survivepopsize = len(population)
    for x in range(0, survivepopsize, 2):
        #one point crossover produce 2 offspring: the parent [1,1,|1,0,0,0] & [1,0,|0,0,1,0] => the offspring [1,1,|0,0,1,0] [1,0,|1,0,0,0]
        if(CROSSOVER_POINT == 1):
            randomslicing = random.randint(1, GENE_SIZE-1)
            offspring1 = population[x].chromosome[0:randomslicing]+population[x+1].chromosome[randomslicing:GENE_SIZE]
            offspring2 = population[x+1].chromosome[0:randomslicing]+population[x].chromosome[randomslicing:GENE_SIZE]
            population.append(Individual(offspring1, "Gen"+str(gen)+" - Chromosome #"+str(x)))
            population.append(Individual(offspring2, "Gen"+str(gen)+" - Chromosome #"+str(x+1)))
        #two point crossover but same index slice: the parent [1,1,|1,0,|0,0] & [1,0,|0,0,|1,0] => the offspring [1,1,|0,0,|0,0] [1,0,|1,0,|1,0]
        else: 
            randomslicing1 = random.randint(1, GENE_SIZE-2)
            randomslicing2 = random.randint(randomslicing1, GENE_SIZE-1)
            offspring1 = population[x].chromosome[0:randomslicing1]+population[x+1].chromosome[randomslicing1:randomslicing2]+population[x].chromosome[randomslicing2:GENE_SIZE]
            offspring2 = population[x+1].chromosome[0:randomslicing1]+population[x].chromosome[randomslicing1:randomslicing2]+population[x+1].chromosome[randomslicing2:GENE_SIZE]
            population.append(Individual(offspring1, "Gen"+str(gen)+" - Chromosome #"+str(x)))
            population.append(Individual(offspring2, "Gen"+str(gen)+" - Chromosome #"+str(x+1)))
        
    return population

#mutation
def mutation(population):
    for x in range(POP_SIZE):
        for y in range(GENE_SIZE):\
            #each gene in each chromosome have a chance to mutate using bitwise
            if(random.random() < MUTATION_RATE):
                population[x].chromosome[y] = 1 - population[x].chromosome[y]
    return population

def printPopulation(population):
    for x in population:
        print(x.geneticinfo+": "+str(x.chromosome))

def printPopulationWithFit(population):
    for x in population:
        print(f"{x.geneticinfo}: {str(x.chromosome)} = X: {x.x}, fitness: {x.fitness}")


def main():
    start_time = time.time()
    population = initialize(POP_SIZE)
    print("--------------------------------------------------")
    print("Initial Population")
    print(f"--------------------------------------------------\n")
    targetchromosome = [1 for x in range(GENE_SIZE)]
    targetfit = chrotodecfit(targetchromosome)
    print("Target Chromosome: ", targetchromosome)
    printPopulation(population)
    print("[Fitness Calculation]")
    fitness_calc(population)
    population.sort(key=sortPopulation, reverse=True) #Sort population descending
    print()
    gen = 1
    while(gen <= GENERATION_LIMIT):
        if(population[0].fitness == targetfit):
            break
        print("--------------------------------------------------")
        print("Generation ",gen)
        print("--------------------------------------------------")
        print("[Sorted Population]")
        printPopulation(population)
        print("[Selection]")
        population=selection(population)
        printPopulationWithFit(population)
        print("[Crossover]")
        population = crossover(population, gen)
        printPopulation(population)
        print("[Mutation]")
        population = mutation(population)
        printPopulation(population)
        print("[Fitness Calculation]")
        fitness_calc(population)
        population.sort(key=sortPopulation, reverse=True)
        print()
        gen += 1
    elapsed_time = time.time() - start_time
    print("Compute Time: ", elapsed_time, " seconds")

main()