import numpy
from GenOpt import GeneticOptimizer
##Booths Function but with an additional slack variable to show the constraint feature.
def BoothsFnc(x):
    return (x[:, 0] + 2*x[:, 1] - 7)**2 + (2*x[:, 0] + x[:, 1] - 5)**2
InitialSolutions = [numpy.array([numpy.random.uniform(), numpy.random.uniform(), numpy.random.uniform()]) for i in range(1000)]
InitialSolutions = numpy.vstack([10*z/sum(z) for z in InitialSolutions])
G2 = GeneticOptimizer(InitialSolutions = InitialSolutions, 
                     Objective = BoothsFnc, 
                     ub = [10,10,10], 
                     lb = [0,0,0], 
                     Sense = 'min', 
                     MutationType = 'Sum Constraint',
                     Crossover = 'Weighted Average')
R = G2.GA()