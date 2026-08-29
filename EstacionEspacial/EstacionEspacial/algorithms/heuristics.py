from typing import Tuple
from algorithms import utils
from algorithms.problems import SystemRepairProblem
import math


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    """
    The Manhattan distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    position, hasKit, pending = state
    if not hasKit:
        target = problem.kitPosition
    elif pending:
        target = min(pending, key=lambda system: abs(position[0] - system[0]) + abs(position[1] - system[1]))
    else:
        target = problem.controlPosition
    
    return abs(position[0] - target[0]) + abs(position[1] - target[1])


def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    position, hasKit, pending = state
    if not hasKit:
        target = problem.kitPosition
    elif pending:
        target = min(pending, key=lambda system: math.hypot(position[0] - system[0], position[1] - system[1]))
    else:
        target = problem.controlPosition

    return math.hypot(position[0] - target[0], position[1] - target[1])


def systemRepairHeuristic(
    state: Tuple[Tuple, bool, Tuple], problem: SystemRepairProblem
):
    """
    Your heuristic for the SystemRepairProblem.

    state: (position, hasKit, pendingSystems)
    problem: SystemRepairProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider the kit, pending systems, and the final return to control center
    - Balance heuristic strength vs. computation time (do experiments!)
    """
    position, hasKit, pending = state
    
    def distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def minSpanningTreeCost(systems):
        cacheKey = ("mst", systems)
              
        if cacheKey in problem.heuristicInfo:
            return problem.heuristicInfo[cacheKey]
        
        if len(systems) <= 1:
            problem.heuristicInfo[cacheKey] = 0
            return 0
        
        visited = {systems[0]}
        totalCost = 0
        
        while len(visited) < len(systems):
            bestCost = float("inf")
            bestSystem = None
            
            for source in visited:
                for target in systems:
                    if target not in visited:
                        edgeCost = distance(source, target)
                        if edgeCost < bestCost:
                            bestCost = edgeCost
                            bestSystem = target
            
            visited.add(bestSystem)
            totalCost += bestCost
        problem.heuristicInfo[cacheKey] = totalCost
        return totalCost
    
    if not pending:
        return distance(position, problem.controlPosition)
    
    systemsCost = (minSpanningTreeCost(pending) + min(distance(system, problem.controlPosition) for system in pending))
    
    if not hasKit:
        return (distance(position, problem.kitPosition) + min(distance(problem.kitPosition, system) for system in pending) + systemsCost)
    
    return (min(distance(position, system) for system in pending) + systemsCost)