# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

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
    # Initialize the frontier with the start state and empty path
    frontier = util.Stack()
    start_state = problem.getStartState()
    frontier.push((start_state, []))  # (state, path_to_state)
    
    # Keep track of visited states to avoid cycles
    visited = set()
    
    while not frontier.isEmpty():
        # Get the current state and path
        current_state, path = frontier.pop()
        
        # Check if we've reached the goal
        if problem.isGoalState(current_state):
            return path
        
        # Skip if we've already visited this state
        if current_state in visited:
            continue
            
        # Mark current state as visited
        visited.add(current_state)
        
        # Get all successors of the current state
        successors = problem.getSuccessors(current_state)
        
        # Add each successor to the frontier
        for next_state, action, cost in successors:
            if next_state not in visited:
                new_path = path + [action]
                frontier.push((next_state, new_path))
    
    # If no solution found, return empty list
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    start_state = problem.getStartState()

    # Trivial case: start is goal
    if problem.isGoalState(start_state):
        return []

    # Each queue entry: (state, path_to_state)
    frontier.push((start_state, []))

    # Track visited states to avoid re-expansion
    visited = set()
    visited.add(start_state)

    while not frontier.isEmpty():
        current_state, path = frontier.pop()

        if problem.isGoalState(current_state):
            return path

        for next_state, action, cost in problem.getSuccessors(current_state):
            if next_state not in visited:
                visited.add(next_state)
                frontier.push((next_state, path + [action]))

    # No path found
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    start_state = problem.getStartState()

    # Each PQ entry: (state, path_to_state, path_cost)
    frontier.push((start_state, [], 0), 0)

    # Record the best known cost to reach each state
    best_cost = {start_state: 0}

    while not frontier.isEmpty():
        state, path, cost_so_far = frontier.pop()

        # If this popped entry is outdated (we've found a cheaper way), skip it
        if cost_so_far > best_cost.get(state, float('inf')):
            continue

        if problem.isGoalState(state):
            return path

        for next_state, action, step_cost in problem.getSuccessors(state):
            new_cost = cost_so_far + step_cost
            if new_cost < best_cost.get(next_state, float('inf')):
                best_cost[next_state] = new_cost
                frontier.push((next_state, path + [action], new_cost), new_cost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    start_state = problem.getStartState()

    # f(start) = g(start)=0 + h(start)
    start_h = heuristic(start_state, problem)
    frontier.push((start_state, [], 0), start_h)

    # Record best known g-costs
    best_cost = {start_state: 0}

    while not frontier.isEmpty():
        state, path, g_cost = frontier.pop()

        # Skip outdated entries
        if g_cost > best_cost.get(state, float('inf')):
            continue

        if problem.isGoalState(state):
            return path

        for next_state, action, step_cost in problem.getSuccessors(state):
            new_g = g_cost + step_cost
            if new_g < best_cost.get(next_state, float('inf')):
                best_cost[next_state] = new_g
                f_score = new_g + heuristic(next_state, problem)
                frontier.push((next_state, path + [action], new_g), f_score)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
