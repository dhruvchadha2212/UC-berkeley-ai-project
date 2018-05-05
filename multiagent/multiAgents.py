# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.

	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best
		print legalMoves
		print scores
		print legalMoves[chosenIndex]
		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		newGhostPosition = successorGameState.getGhostPositions()
		foodPositions = newFood.asList()
		minDistFood = float("inf")
		ghostPositions = newGhostPosition
		minDistGhost = float("inf")
		for food in foodPositions:
			minDistFood = float(min(minDistFood, abs(food[0] - newPos[0]) + abs(food[1] - newPos[1])))
		for ghost in ghostPositions:
			minDistGhost = float(min(minDistGhost, abs(ghost[0] - newPos[0]) + abs(ghost[1] - newPos[1])))
		if minDistFood == 0 or minDistGhost == 0:
			value = -float("inf")
		else:
			value = float(1/minDistFood) - 5*float(1/minDistGhost)

		return successorGameState.getScore() + value

def scoreEvaluationFunction(currentGameState):
	"""
	  This default evaluation function just returns the score of the state.
	  The score is the same one displayed in the Pacman GUI.

	  This evaluation function is meant for use with adversarial search agents
	  (not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.  Please do not
	  remove anything, however.

	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)
		self.actionCost = {}

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent (question 2)
	"""
	
	def maxValue(self, plyCount, gameState, agentIndex):
		v = float("-inf")
		legalActions = gameState.getLegalActions(agentIndex)
		for action in legalActions:
			successorGameState = gameState.generateSuccessor(agentIndex, action)
			val = self.value(plyCount, successorGameState, agentIndex + 1)
			if plyCount == 0:
				self.actionCost[action] = val
			v = max(v, val)
		# if v == float("inf"):
		# print "pacman", gameState.getLegalActions(agentIndex), legalActions
		# print plyCount
		# print v
		# print gameState
		return v

	def minValue(self, plyCount, gameState, agentIndex):
		legalActions = gameState.getLegalActions(agentIndex)
		if len(legalActions) == 0:
			return self.evaluationFunction(gameState)
		v = float("inf")
		nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
		for action in legalActions:
			successorGameState = gameState.generateSuccessor(agentIndex, action)
			v = min(v, self.value(plyCount + (1 if (nextAgentIndex == 0) else 0), successorGameState, nextAgentIndex))
		# if v == float("inf"):
		# print "ghost", agentIndex, gameState.getLegalActions(agentIndex), legalActions
		# print plyCount
		# print v
		# print gameState
		return v

	def value(self, plyCount, gameState, agentIndex):
		if plyCount == self.depth:
			return self.evaluationFunction(gameState)
		if agentIndex == 0:
			return self.maxValue(plyCount, gameState, agentIndex)
		return self.minValue(plyCount, gameState, agentIndex)

	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.

		  Here are some method calls that might be useful when implementing minimax.

		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		self.actionCost = {}
		maxval = self.value(0, gameState, 0)
		for action in self.actionCost:
			if self.actionCost[action] == maxval:
				return action
		return Directions.STOP
		util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""
	def maxValue(self, plyCount, gameState, agentIndex, alpha, beta):
		v = float("-inf")
		legalActions = gameState.getLegalActions(agentIndex)
		for action in legalActions:
			successorGameState = gameState.generateSuccessor(agentIndex, action)
			val = self.value(plyCount, successorGameState, agentIndex + 1, alpha, beta)
			if plyCount == 0:
				self.actionCost[action] = val
			v = max(v, val)
			if v > beta:
				return v
			alpha = max(alpha, v)
		return v

	def minValue(self, plyCount, gameState, agentIndex, alpha, beta):
		legalActions = gameState.getLegalActions(agentIndex)
		if len(legalActions) == 0:
			return self.evaluationFunction(gameState)
		v = float("inf")
		nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
		for action in legalActions:
			successorGameState = gameState.generateSuccessor(agentIndex, action)
			val = self.value(plyCount + (1 if (nextAgentIndex == 0) else 0), successorGameState, nextAgentIndex, alpha, beta)
			v = min(v, val)
			if v < alpha:
				return v
			beta = min(beta, v)
		return v

	def value(self, plyCount, gameState, agentIndex, alpha, beta):
		if plyCount == self.depth:
			return self.evaluationFunction(gameState)
		if agentIndex == 0:
			return self.maxValue(plyCount, gameState, agentIndex, alpha, beta)
		return self.minValue(plyCount, gameState, agentIndex, alpha, beta)

	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		self.actionCost = {}
		maxval = self.value(0, gameState, 0, float("-inf"), float("inf"))
		for action in self.actionCost:
			if self.actionCost[action] == maxval:
				return action
		util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
	def maxValue(self, plyCount, gameState, agentIndex):
		v = float("-inf")
		legalActions = gameState.getLegalActions(agentIndex)
		for action in legalActions:
			successorGameState = gameState.generateSuccessor(agentIndex, action)
			val = self.value(plyCount, successorGameState, agentIndex + 1)
			if plyCount == 0:
				self.actionCost[action] = val
			v = max(v, val)
		return v

	def expValue(self, plyCount, gameState, agentIndex):
		legalActions = gameState.getLegalActions(agentIndex)
		if len(legalActions) == 0:
			return self.evaluationFunction(gameState)
		nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
		v = 0
		probability = []
		sum = 0.0
		for i in range(0, len(legalActions)):
			random_number = random.random()
			sum += random_number
			probability.append(random_number)
		
		for i in range(0, len(legalActions)):
			probability[i] = float(probability[i])/float(sum)

		index = 0
		for action in legalActions:
			successorGameState = gameState.generateSuccessor(agentIndex, action)
			v += float(probability[index]) * float(self.value(plyCount + (1 if (nextAgentIndex == 0) else 0), successorGameState, nextAgentIndex))
			index += 1
		return v

	def value(self, plyCount, gameState, agentIndex):
		if plyCount == self.depth:
			return self.evaluationFunction(gameState)
		if agentIndex == 0:
			return self.maxValue(plyCount, gameState, agentIndex)
		return self.expValue(plyCount, gameState, agentIndex)

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		"*** YOUR CODE HERE ***"
		self.actionCost = {}
		maxval = self.value(0, gameState, 0)
		for action in self.actionCost:
			if self.actionCost[action] == maxval:
				return action
		util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	print currentGameState.data

	pacmanPosition = currentGameState.getPacmanPosition()
	ghostPositions = currentGameState.getGhostPositions()
	foodPositions = currentGameState.getFood().asList()
	
	val = 0.0
	for pos in ghostPositions:
		manDist = 0.1 + float(abs(pacmanPosition[0] - pos[0]) + abs(pacmanPosition[1] - pos[1]))
		val -= 10 / float(manDist)

	foodLen = []
	for pos in foodPositions:
		manDist = float(abs(pacmanPosition[0] - pos[0]) + abs(pacmanPosition[1] - pos[1]))
		foodLen.append(manDist)
	foodLen.append(1000)

	foodLen.sort()

	val += 1.0/foodLen[1]

	return val
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

