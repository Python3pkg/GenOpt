import numpy
import random
import heapq
from itertools import izip_longest
class GeneticOptimizer:
    """Optimizes the objective function utilizing a genetic algorithm."""
    def __init__(self, InitialSolutions, Objective, lb, ub, MutationType = 'Random',
                 MutationRate = .01, Sense = 'min', Crossover = 'Quadratic', maxIterations = 250):
        """
            InitialSolutions: numpy array with shape (num_sols, num_variables). If there is a linear constraint, the initial solution
                              must conform to the constraints. 
            Objective: The objective function to be optimized.
            lb: list of lower bounds for each variable
            ub: list of upper bound for each variable
            MutationType: The method of mutation. Choices are Random and Sum Constraint. The latter is used for maintaining
                          a linear constraint.
            MutationRate: The probability of mutating a gene
            Sense: min or max
            Crossover: The type of crossover. Choices are Quadratic, Weighted Average, and Heuristic. Weighted Average is the only
                       crossover capable of maintaining a linear constraint.
            maxIterations: total number of iterations before termination
        """
        self.InitialSolutions = InitialSolutions
        self.MutationType = MutationType
        self.MutationRate = MutationRate
        self.Objective = Objective
        self.lb = lb
        self.ub = ub
        self.Sense = Sense
        self.Crossover = Crossover
        self.num_sols = len(self.InitialSolutions)
        self.maxIterations = maxIterations

    def GA(self):
        """Optimizes the objective function. Returns two objects: a tuple of the optimal variables and optimal value, and
           an object detailing the best and average score at each iteration."""
        Fitness = self.Objective(self.InitialSolutions)
        Sol_Fit = list(zip(self.InitialSolutions, Fitness))
        Iterations = 0
        self.SolMetrics = []
        while Iterations < self.maxIterations:
            Sol_Fit.sort(key = lambda x: x[1])
            
            ##Quadratic needs to be run differently than other crossovers because it takes 3 parents to make a child
            if self.Crossover == 'Quadratic':
                ##Future versions could have a roulette wheel selection. Currently just use top scores.
                if self.Sense == 'min':
                    Sol_Fit = Sol_Fit[:-self.num_sols/4]
                else:
                    Sol_Fit = Sol_Fit[self.num_sols/4:]
                IndexPairs = self.CreatePairs(list(range(self.num_sols-self.num_sols/4)), 3)
                NextGenSols = numpy.empty((self.num_sols/4, len(self.InitialSolutions[0])))
                for i, (Index1, Index2, Index3) in enumerate(IndexPairs):
                    Child = self.Crossover_Quadratic(Sol_Fit[Index1], Sol_Fit[Index2], Sol_Fit[Index3])
                    MutatedChild = self.Mutate_Random(Child)
                    NextGenSols[i] = MutatedChild
            elif self.Crossover in ['Weighted Average', 'Heuristic']:
                if self.Sense == 'min':
                    Sol_Fit = Sol_Fit[:-self.num_sols/2]
                else:
                    Sol_Fit = Sol_Fit[self.num_sols/2:]
                    
                IndexPairs = self.CreatePairs(list(range(self.num_sols/2)), 2)
                NextGenSols = numpy.empty((self.num_sols/2, len(self.InitialSolutions[0])))
                
                i = 0
                for Index1, Index2 in IndexPairs:
                    if self.Crossover == 'Weighted Average':
                        Child1 = self.Crossover_WeightedAverage(Sol_Fit[Index1][0], Sol_Fit[Index2][0])
                        Child2 = self.Crossover_WeightedAverage(Sol_Fit[Index1][0], Sol_Fit[Index2][0])
                    elif self.Crossover == 'Heuristic':                    
                        Child1 = self.Crossover_Heuristic(Sol_Fit[Index1], Sol_Fit[Index2])
                        Child2 = self.Crossover_Heuristic(Sol_Fit[Index1], Sol_Fit[Index2])
                    
                    if self.MutationType == 'Random':
                        MutatedChild1 = self.Mutate_Random(Child1)
                        MutatedChild2 = self.Mutate_Random(Child2)
                    elif self.MutationType == 'Sum Constraint':
                        MutatedChild1 = self.Mutate_SumConstraint(Child1)
                        MutatedChild2 = self.Mutate_SumConstraint(Child2)
                    
                    NextGenSols[i] = MutatedChild1
                    NextGenSols[i+1] = MutatedChild2
                    i += 2
            
            Fitness = self.Objective(NextGenSols)
            if self.Sense == 'min':
                self.SolMetrics.append( (min(Fitness), numpy.mean(Fitness)) )  
            else:
                self.SolMetrics.append( (max(Fitness), numpy.mean(Fitness)) )
            New_Sol_Fit = list(zip(NextGenSols, Fitness))
            Sol_Fit.extend(New_Sol_Fit)
    
            Iterations += 1
        if self.Sense == 'min':
            return min(Sol_Fit, key = lambda x: x[1]), self.SolMetrics
        else:
            return max(Sol_Fit, key = lambda x: x[1]), self.SolMetrics
            
    def Mutate_Random(self, Sol):
        """Each variable has a self.MutationRate probability of being altered to a random uniform number between lb and ub."""
        for Index in range(len(Sol)):
            if numpy.random.uniform() < self.MutationRate:
                Value = numpy.random.uniform(low = self.lb[Index] , high = self.ub[Index])
                Sol[Index] = Value
        return Sol
        
    def Mutate_SumConstraint(self, Sol):
        """A single variable will be randomly assigned to be lb or ub. Then, the other variables are adjusted
           in order to maintain the linear constraint."""
        if numpy.random.uniform() < self.MutationRate:
            Index = random.randrange(len(Sol))
            Value = numpy.random.choice((self.lb[Index], self.ub[Index]))
            NeedToSumTo = sum(Sol)-Value        
            
            Mask = numpy.ones_like(Sol, numpy.bool)   
            Mask[Index] = False
            S_Remainder = sum(Sol[Mask])
            
            for i in range(len(Sol)):
                if i == Index:
                    Sol[i] = Value
                else:
                    if self.is_close(S_Remainder,0):
                        ##Division by zero
                        Sol[i] = 0
                    else:
                        Sol[i] = (Sol[i]/S_Remainder)*NeedToSumTo
        return Sol

    def is_close(self, a, b, rtol=1e-05, atol=1e-08):
        return abs(a - b) <= (atol + rtol * abs(b))

    def _GetHeuristicPoint(self, Better, Worse, lb, ub, r, w):
        """Utility function used in the heuristic and quadratic crossovers. Uses recursion in case the solution is infeasible, 
           and returns random assignment between the two parents if no feasible solution after 10 attempts."""
        if w > 10:
            return numpy.random.choice([Better, Worse])
        Point = r*(Better-Worse)+Better
        if lb <= Point <= ub:
            return Point
        else:
            ##Recursion until an acceptable answer is made OR w = 10 and randomly assign
            return self._GetHeuristicPoint(Better, Worse, lb, ub, r/2.0, w+1)           
           
    def Crossover_Quadratic(self, xxx_todo_changeme, xxx_todo_changeme1, xxx_todo_changeme2):
        """Takes the fitness scores of the three parents and finds the point most likely to maximize fitness using basic calculus.
           If the resulting solution is infeasible, the heuristic crossover is used on the two best parents.
           It's an obscure crossover but very effective. It is found in a masters MIT thesis here:
           https://dspace.mit.edu/bitstream/handle/1721.1/10930/35651641-MIT.pdf?sequence=2"""
        (Sol1, f1) = xxx_todo_changeme
        (Sol2, f2) = xxx_todo_changeme1
        (Sol3, f3) = xxx_todo_changeme2
        Child = numpy.empty((len(Sol1), ))
        for i, (s1, s2, s3) in enumerate(list(zip(Sol1, Sol2, Sol3))):
            a_j = (1.0/(s3-s2))*( (f3-f1)/float(s3-s1) - (f2-f1)/float(s2-s1) )
            b_j = (f2-f1)/float(s2-s1) - a_j*(s2+s1)
            CriticalPoint = -b_j/(2.0*a_j)
            
            if self.Sense == 'min':
                DerivTest = 2*a_j > 0
            else:
                DerivTest = 2*a_j < 0
                
            if DerivTest and (self.lb[i] <= CriticalPoint <= self.ub[i]):
                Child[i] = CriticalPoint
            else:
                ##Do heuristic crossover if CriticalPoint isn't possible
                ##Heuristic crossover by itself is pretty good.
                r = numpy.random.uniform()
                if self.Sense == 'min':
                    (f_1st, s_1st), (f_2nd, s_2nd) = heapq.nsmallest(2, [(f1, s1),(f2, s2),(f3, s3)])
                else:
                    (f_1st, s_1st), (f_2nd, s_2nd) = heapq.nlargest(2, [(f1, s1),(f2, s2),(f3, s3)])
                Child[i] = self._GetHeuristicPoint(s_1st, s_2nd, self.lb[i], self.ub[i], r, 1)
        return Child
        
    def CreatePairs(self, iterable, n):
        """Breaks iterable into chunks of size n"""
        args = [iter(iterable)] * n
        return izip_longest(*args)
        
    def Crossover_WeightedAverage(self, Sol1, Sol2):
        """Picks a point randoly between the genes."""
        Beta = numpy.random.uniform()
        Child = Beta*Sol1+(1-Beta)*Sol2
        return Child

    def Crossover_Heuristic(self, xxx_todo_changeme3, xxx_todo_changeme4, lb, ub, Sense):
        """Uses this formula: r*(Better-Worse)+Better, where r is a random number between 0 and 1"""
        (Sol1, f1) = xxx_todo_changeme3
        (Sol2, f2) = xxx_todo_changeme4
        Child = numpy.empty((len(Sol1), ))
        for i, (s1, s2) in enumerate(list(zip(Sol1, Sol2))):
            if ((Sense == 'min') & (f1<f2)) or ((Sense == 'max') & (f1>f2)):
                Child[i] = self._GetHeuristicPoint(s1, s2, lb[i], ub[i], numpy.random.uniform(), 1)
            else:
                Child[i] = self._GetHeuristicPoint(s2, s1, lb[i], ub[i], numpy.random.uniform(), 1) 
        return Child