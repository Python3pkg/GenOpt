# GenOpt
Contains a *class* for optimizing analytic functions utilizing a **genetic algorithm**.

## Installation
  ```
  pip install GenOpt
  ```
  
### Dependencies
* numpy
* random
* heapq
* itertools

## Usage

### Arguments
*The GeneticOptimizer class requires several inputs:*

> **InitialSolutions**: An array of initial solutions. If you need a summary constraint to be respected (e.g. x1+x2 = 1) then each initial solution must conform to the constraint.

> **Objective**: The objective function to be optimized. 

> **lb**: List of lower bounds for each variable

> **ub**: List of upper bounds for each variable

> **MutationType**: Choice of `'Random'` or `'Sum Constraint'`. The former uniformly randomly assigns a gene to between lb and ub. The latter does the same and then repairs the rest of the solution to respect a linear constraint. [Default: `'Random'`] 

> **MutationRate** = The rate at which genes are mutated [Default: `.01`]

> **Sense**: `'min'` or `'max'` [Default: `'min'`]

> **Crossover**: Choice of `'Quadratic'`, `'Heuristic'`, and `'Weighted Average'`. Quadratic is typically best, and Weighted Average is the only one that can respect a linear constraint (use in conjunction with MutationType = 'Sum Constraint') [Default: `'Quadratic'`]

> **maxIterations**: The number of generations before algorithm termination [Default: `250`]

### Outputs
There are **two** outputs from `GeneticOptimizer.GA()`: The first is the *optimal solution* and the *optimal value*, and the second is the *best and average value at each generation*.

### Examples

  ###### Unconstrained Optimization
  ```
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
  ```
  
  ###### Constrained Optimization
  ```
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
  ```

## Reference

Adewuya, A. (1996) "New Methods in Genetic Search with Real-Valued Chromosomes". Submitted to the Department of Mechanical Engineering in Partial Fulfillment of the Requirements for the Degree of Master of Science in Mechanical Engineering at the Massachusetts Institute of Technology. pp. 31-52.
