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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        successorGameState = currentGameState.generatePacmanSuccessor(action) # mapa con pacman, fantasma, cocos y puntuación (del estado sucesor)
        print("successorGameState = " + str(successorGameState))
        newPos = successorGameState.getPacmanPosition() # posición (x, y)
        print("newPos = " + str(newPos))
        newFood = successorGameState.getFood() # comida true/false (grid)
        print("newFood = " + str(newFood))
        newGhostStates = successorGameState.getGhostStates()
        print("newGhostStates = " + str(newGhostStates)) # estado de los fantasmas (como si fuera pacmnan
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        print("newScaredTimes = " + str(newScaredTimes))

        "*** YOUR CODE HERE ***"
        # Calcular distancia con la comida más cercana
        dist_comida_min = -1 # valor por defecto para indicar que todavía no tiene valor
        for i in newFood.asList():
            distancia_actual_comida = manhattanDistance(newPos, i)
            if dist_comida_min == -1:
                dist_comida_min = distancia_actual_comida
            else:
                if distancia_actual_comida < dist_comida_min:
                    dist_comida_min = distancia_actual_comida
        puntuacion_pos = (120 - dist_comida_min) * len(newGhostStates)
        # Calcular distancia con la comida más cercana
        dist_total_fantasmas = 0
        for ghost in newGhostStates:
            pos_fantasma = ghost.getPosition()
            distancia_actual_fantasma = manhattanDistance(newPos, pos_fantasma)
            dist_total_fantasmas += distancia_actual_fantasma
        puntuacion_neg = 10 - dist_total_fantasmas

        valor_final = puntuacion_pos - puntuacion_neg
        print(valor_final)
        return valor_final
        #return successorGameState.getScore()

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        mejor_accion = None
        v_max = float('-inf')
        profundidad = 1
        acciones_legales = gameState.getLegalActions(0)
        for accion in acciones_legales:
            siguiente_estado = gameState.generateSuccessor(0, accion)
            v_actual = self.min_value(siguiente_estado, 1, profundidad)
            if v_actual > v_max:
                v_max = v_actual
                mejor_accion = accion
        return mejor_accion

        #util.raiseNotDefined()

    def max_value(self, gameState, profundidad):
        v = float('-inf')
        if gameState.isWin() or gameState.isLose():
            v = self.evaluationFunction(gameState)
            return v
        acciones_legales = gameState.getLegalActions(0)
        for accion in acciones_legales:
            siguiente_estado = gameState.generateSuccessor(0, accion)
            v = max(v, self.min_value(siguiente_estado, 1, profundidad))
        return v

    def min_value(self, gameState, agente_ind, profundidad):
        v = float('inf')
        if gameState.isWin() or gameState.isLose():
            v = self.evaluationFunction(gameState)
            return v
        acciones_legales = gameState.getLegalActions(agente_ind)
        for accion in acciones_legales:
            siguiente_estado = gameState.generateSuccessor(agente_ind, accion)
            if agente_ind == gameState.getNumAgents() - 1:
                if profundidad == self.depth:
                    v = min(v, self.evaluationFunction(siguiente_estado))
                else:
                    v = min(v, self.max_value(siguiente_estado, profundidad + 1))
            else:
                v = min(v, self.min_value(siguiente_estado, agente_ind + 1, profundidad))
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        mejor_accion = None
        v_max = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        profundidad = 1
        acciones_legales = gameState.getLegalActions(0)
        for accion in acciones_legales:
            siguiente_estado = gameState.generateSuccessor(0, accion)
            v_actual = self.min_value(siguiente_estado, 1, profundidad, alpha, beta)
            if v_actual > v_max:
                v_max = v_actual
                mejor_accion = accion

            if v_max > beta:
                return mejor_accion
            alpha = max(alpha, v_max)
        return mejor_accion

        #util.raiseNotDefined()

    def max_value(self, gameState, profundidad, alpha, beta):
        v = float('-inf')
        if gameState.isWin() or gameState.isLose():
            v = self.evaluationFunction(gameState)
            return v
        acciones_legales = gameState.getLegalActions(0)
        for accion in acciones_legales:
            siguiente_estado = gameState.generateSuccessor(0, accion)
            v = max(v, self.min_value(siguiente_estado, 1, profundidad, alpha, beta))

            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, gameState, agente_ind, profundidad, alpha, beta):
        v = float('inf')
        if gameState.isWin() or gameState.isLose():
            v = self.evaluationFunction(gameState)
            return v
        acciones_legales = gameState.getLegalActions(agente_ind)
        for accion in acciones_legales:
            siguiente_estado = gameState.generateSuccessor(agente_ind, accion)
            if agente_ind == gameState.getNumAgents() - 1:
                if profundidad == self.depth:
                    v = min(v, self.evaluationFunction(siguiente_estado))
                else:
                    v = min(v, self.max_value(siguiente_estado, profundidad + 1, alpha, beta))
            else:
                v = min(v, self.min_value(siguiente_estado, agente_ind + 1, profundidad, alpha, beta))

            if v < alpha:
                return v
            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
