from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic


def tinyDiagnosticSearch(problem: SearchProblem):
    """
    Returns a hard-coded sequence of moves for the tinyDiagnostic layout.
    For any other station layout, the sequence of moves will be incorrect.
    """
    s = Directions.SOUTH
    e = Directions.EAST
    return [s, e, s, e, e, e, e, s, e, e, s, s, e, s, s, e, s, e, e, e, e, e, e, e]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    stack = utils.Stack()
    visited = set()
    
    start = problem.getStartState()
    stack.push((start, []))
    
    while not stack.isEmpty():
        state, actions = stack.pop()

        if state in visited:
            continue

        visited.add(state)

        if problem.isGoalState(state):
            return actions

        for successor, action, cost in problem.getSuccessors(state):
            if successor not in visited:
                stack.push((successor, actions + [action]))

    return []



def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    queue = utils.Queue()
    visited = set()

    start = problem.getStartState()
    queue.push((start, []))

    while not queue.isEmpty():
        state, actions = queue.pop()

        if state in visited:
            continue

        visited.add(state)

        if problem.isGoalState(state):
            return actions

        for successor, action, cost in problem.getSuccessors(state):
            if successor not in visited:
                queue.push((successor, actions + [action]))

    return []


def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """
    frontera = utils.PriorityQueue()
    estadoInicial = problem.getStartState()
    frontera.push((estadoInicial, [], 0), 0)

    visitados = set()

    while not frontera.isEmpty():
        estado, acciones, costo = frontera.pop()

        if problem.isGoalState(estado):
            return acciones

        if estado in visitados:
            continue
        visitados.add(estado)

        for estadoSiguiente, accion, costoPaso in problem.getSuccessors(estado):
            if estadoSiguiente not in visitados:
                costoNuevo = costo + costoPaso
                frontera.push((estadoSiguiente, acciones + [accion], costoNuevo), costoNuevo)

    return []


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    border = utils.PriorityQueue()
    start = problem.getStartState()
    bestCost = {start: 0}
    
    border.push((start, [], 0), heuristic(start, problem))
    
    while not border.isEmpty():
        state, actions, cost = border.pop()
        if cost != bestCost.get(state):
            continue
        if problem.isGoalState(state):
            return actions

        for next, action, stepCost in problem.getSuccessors(state):
            newCost = cost + stepCost
            if next not in bestCost or newCost < bestCost[next]:
                bestCost[next] = newCost
                priority = newCost + heuristic(next, problem)
                border.push((next, actions + [action], newCost), priority)
    return []


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
