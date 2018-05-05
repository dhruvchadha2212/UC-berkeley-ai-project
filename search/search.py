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
from util import *

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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:"""
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    
    st = Stack()
    path = []
    visited = {}
    opposite = {'East':'West', 'West':'East', 'North':'South', 'South':'North'}
    start = (problem.getStartState(), '', 0)
    st.push(start)
    visited[start] = True
    while st.isEmpty() == False:
        nbrs = problem.getSuccessors(st.top()[0])
        topush = ()
        for nxt in nbrs:
            if nxt not in visited:
                topush = nxt
                break
        if topush == ():
            if st.top() != start:
                path.append(opposite[st.top()[1]])
            st.pop()
        else:
            st.push(topush)
            visited[topush] = True
    return path
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    path, visited, parent = [], {}, {}
    opposite = {'East':'West', 'West':'East', 'North':'South', 'South':'North'}
    start = (problem.getStartState(), '', 0, ())
    q = Queue()
    q.push(start)
    visited[start] = True
    while q.isEmpty() == False:
        nbrs = problem.getSuccessors(q.front()[0], q.front()[3])
        for nxt in nbrs:
            if nxt not in visited:
                q.push(nxt)
                parent[nxt] = q.front()
                visited[nxt] = 1
            if problem.isGoalState(nxt[0], nxt[3]):
                curr = nxt
                while curr != start:
                    path.insert(0, curr[1])
                    curr = parent[curr]
                return path
        q.pop()
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    path = []
    visited = {}
    opposite = {'East':'West', 'West':'East', 'North':'South', 'South':'North'}
    parent = {}
    priority = {}
    start = (problem.getStartState(), '', 0)
    pq = PriorityQueue()
    priority[start] = start[2]
    pq.push(start, priority[start])
    visited[start] = True
    while pq.isEmpty() == False:
        nbrs = problem.getSuccessors(pq.front()[0])
        for nxt in nbrs:
            if nxt not in visited:
                priority[nxt] = nxt[2] + priority[pq.front()]
                pq.push(nxt, priority[nxt])
                parent[nxt] = pq.front()
                visited[nxt] = 1
            if problem.isGoalState(nxt[0]):
                curr = nxt
                while curr != start:
                    path.insert(0, curr[1])
                    curr = parent[curr]
                return path
        pq.pop()
    util.raiseNotDefined()

def nullHeuristic(state, problem=None, visitOrder=()):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    path = []
    visited = {}
    opposite = {'East':'West', 'West':'East', 'North':'South', 'South':'North'}
    parent = {}
    actualDist = {}
    priority = {}
    start = (problem.getStartState(), '', 0, problem.getStartFood())
    pq = PriorityQueue()
    actualDist[start] = start[2]
    priority[start] = actualDist[start] + heuristic(start[0], problem, start[3])
    pq.push(start, priority[start])
    visited[(start[0], start[3])] = True
    while pq.isEmpty() == False:
        nbrs = problem.getSuccessors(pq.front()[0], pq.front()[3])
        for nxt in nbrs:
            if (nxt[0], nxt[3]) not in visited:
                actualDist[nxt] = actualDist[pq.front()] + nxt[2]
                priority[nxt] = actualDist[nxt] + heuristic(nxt[0], problem, nxt[3])
                pq.push(nxt, priority[nxt])
                parent[(nxt[0], nxt[3])] = pq.front()
                visited[(nxt[0], nxt[3])] = True
            if problem.isGoalState(nxt[0], nxt[3]):
                curr = nxt
                while curr != start:
                    path.insert(0, curr[1])
                    curr = parent[(curr[0], curr[3])]
                return path
        pq.pop()
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
