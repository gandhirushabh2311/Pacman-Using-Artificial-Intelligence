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
         #Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        pacmanPosition=successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        foodList=newFood.asList()
        newGhostStates = successorGameState.getGhostStates()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        sumDistanceFactor=0
        foodFactor=1
        ghostIsNear = False
        result=0
        ghostDistances=[]
        

        if action=='Stop':
            return 0
        
        
        for ghost in newGhostStates:
            ghostPosition=ghost.getPosition()
            if ghost.scaredTimer==0 and abs(pacmanPosition[0]-ghostPosition[0])<=3 and abs(pacmanPosition[1]-pacmanPosition[1])<=3:
                ghostIsNear=True
                distance=util.manhattanDistance(pacmanPosition, ghostPosition)
                ghostDistances.append(distance)
                
            if ghostIsNear:
                result=min(ghostDistances)
            else:
                if len(foodList) > 0:
                    distance, closestFood = min([(manhattanDistance(newPos,food),food) for food in foodList])
                    if not distance==0:
                        result+=(1.0/distance)
                    else:
                        result+=10
        return result
            
#        if currentGameState.isWin():
#            return float("inf")
#        if currentGameState.isLose():
#            return - float("inf")
#        score = scoreEvaluationFunction(currentGameState)
#        newFood = currentGameState.getFood()
#        foodPos = newFood.asList()
#        closestfood = float("inf")
#        for pos in foodPos:
#            thisdist = util.manhattanDistance(pos, currentGameState.getPacmanPosition())
#            if (thisdist < closestfood):
#                closestfood = thisdist
#        numghosts = currentGameState.getNumAgents() - 1
#        i = 1
#        disttoghost = float("inf")
#        while i <= numghosts:
#            nextdist = util.manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(i))
#            disttoghost = min(disttoghost, nextdist)
#            i += 1
#        score += max(disttoghost, 4) * 2
#        score -= closestfood * 1.5
#        capsulelocations = currentGameState.getCapsules()
#        score -= 4 * len(foodPos)
#        score -= 3.5 * len(capsulelocations)
#        return score
        
        	  

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
        """
        
                    

            
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def maxValue(gameState,alpha,beta,depth):
            if gameState.isWin() or gameState.isLose() or depth==0:
                return self.evaluationFunction(gameState)
            v=-(float('inf'))
            legalActions=gameState.getLegalActions(0)
            for action in legalActions:
                nextState=gameState.generateSuccessor(0,action)
                v=max(v,minValue(nextState,alpha,beta,gameState.getNumAgents()-1,depth))
                if v >=beta:
                    return v
                alpha=max(alpha,v)
                return v
                    
        def minValue(gameState,alpha,beta,agentindex,depth):
            numGhosts=gameState.getNumAgents()-1
            if gameState.isWin() or gameState.isLose() or depth==0:
                return self.evaluationFunction(gameState)
            v=float("inf")
            legalActions=gameState.getLegalActions(agentindex)
            for action in legalActions:
                nextState=gameState.generateSuccessor(agentindex,action)
                if agentindex==numGhosts : 
                    v=min(v,maxValue(nextState,alpha,beta,depth-1))
                    if v<=alpha:
                        return v
                    beta=min(beta,v)
                else:
                    v=min(v,minValue(nextState,alpha,beta,agentindex+1,depth))
                    if v<=alpha:
                        return v
                    beta=min(beta,v)
            return v
            
        legalActions=gameState.getLegalActions(0)
        bestAction=Directions.STOP
        score=-float('inf')
        alpha=-float('inf')
        beta=float('inf')
        for action in legalActions:
            nextState=gameState.generateSuccessor(0,action)
            prevScore=score
            score=max(score,minValue(nextState,alpha,beta,1,self.depth))
            if score>prevScore:
                bestaction=action
        return bestaction
        
        
        util.raiseNotDefined()

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
        def expectedValue(gameState,agentindex,depth):
            if gameState.isWin() or gameState.isLose() or depth==0:
                return self.evaluationFunction(gameState)
            numGhosts=gameState.getNumAgents()-1
            legalActions=gameState.getLegalActions(agentindex)
            numActions=len(legalActions)
            
            for action in legalActions:
                nextState=gameState.generateSuccessor(agentindex,action)
                if agentindex==numGhosts:
                    newMax=maxValue(nextState,depth-1)
                    totalValue = newMax
                else:
                    totalValue=expectedValue(nextState,agentindex+1,depth)
                    
            return totalValue/numActions
            
        def maxValue(gameState,depth):
            if gameState.isWin() or gameState.isLose() or depth==0:
                return self.evaluationFunction
            legalActions=gameState.getLegalActions(0)
            value=-float("inf")
        
            for action in  legalActions:
                nextState=gameState.generateSuccessor(0,action)
                value=max(value,expectedValue(nextState,1,depth))
                
            return value
            
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction
        value=-float("inf")
        legalActions=gameState.getLegalActions(0)
        bestAction=Directions.STOP
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            prevscore = value
            value = max(value, expectedValue(nextState, 1, self.depth))
            if value > prevscore:
                bestAction = action
        return bestAction
            
                
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

