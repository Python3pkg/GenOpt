import numpy
from GenOpt import GeneticOptimizer
def StyblinskiTang_Fnc(x):
    return (x[:, 0]**4-16*x[:, 0]**2 + 5*x[:, 0])/2.0 + (x[:, 1]**4-16*x[:, 1]**2 + 5*x[:, 1])/2.0
InitialSolutions = numpy.vstack([numpy.array([numpy.random.uniform(), 
                                              numpy.random.uniform()]) for i in range(1000)])
G1 = GeneticOptimizer(InitialSolutions = InitialSolutions, 
                     Objective = StyblinskiTang_Fnc, 
                     ub = [5,5], 
                     lb = [-5,-5], 
                     Sense = 'min', 
                     Crossover = 'Quadratic')
R = G1.GA()
