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
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print(prevFood)
        #print(successorGameState)
        #print(newPos)
        #print(newFood)
        #print(newGhostStates)
        #print(newScaredTimes)

        #Description: Let Food = Ghost = 5

        score = successorGameState.getScore()

        #only consider the closest ghost
        closestGhost = newGhostStates[0].getPosition()
        disToGhost = manhattanDistance(newPos, closestGhost)
        #prevent zeroDivisionError
        if disToGhost > 0:
            score = score - 5 / disToGhost

        #only consider the closest food
        disToFoodList = []
        for x in newFood.asList():
            disToFoodList.append(manhattanDistance(newPos, x))
        if len(disToFoodList):
            if min(disToFoodList) > 0:
                score = score + 5 / min(disToFoodList)

        return score
        

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

        def updateFunction(state, depth, agent):

            #update depth, agent
            if agent >= state.getNumAgents():
                depth += 1
                agent = 0

            #Base case
            if (depth==self.depth or state.isWin() or state.isLose()):
                return self.evaluationFunction(state)

            #decide max or min function 
            if (agent == 0):
                #Pacman action
                return maxValue(state, depth, agent)
            else:
                #Ghost action
                return minValue(state, depth, agent)



        def maxValue(state, depth, agent):
            """
            #check base case
            if  depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), "nonextMove"
            """
            storeList = ["nothing", -float("inf")]

            nextmoves = state.getLegalActions(agent)

            #choose one of the best options
            for move in nextmoves:
            
                nowVal = updateFunction(state.generateSuccessor(agent, move), depth, agent+1)

                #handle different no. of actions
                immedVal = checker(nowVal)

                #deciding correct moves
                if immedVal > storeList[1]:
                    storeList = [move, immedVal]

                #print(storeList)

            return storeList

        def minValue(state, depth, agent):
            """
            #check base case
            if  depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), "nonextMove"
            """
            storeList = ["nothing", float("inf")]

            nextmoves = state.getLegalActions(agent)
            
            #choose one of the best options
            for move in nextmoves:
            
                nowVal = updateFunction(state.generateSuccessor(agent, move), depth, agent+1)

                #handle different no. of actions
                immedVal = checker(nowVal)

                #deciding correct moves
                if immedVal < storeList[1]:
                    storeList = [move, immedVal]

                #print(storeList)

            return storeList

        def checker(nowVal):
            #one 
            if type(nowVal) is not list:
                return nowVal
            #more than one ->choose the first one out of list
            else:
                return nowVal[1]
        

        
        ansList = updateFunction(gameState, 0, 0)
        return ansList[0]

        util.raiseNotDefined()



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def updateFunction(state, depth, agent, a, b):

            #update depth, agent
            if agent >= state.getNumAgents():
                depth += 1
                agent = 0

            #Base case
            if (depth==self.depth or state.isWin() or state.isLose()):
                return self.evaluationFunction(state)

            #decide max or min function 
            if (agent == 0):
                return maxValue(state, depth, agent, a, b)
            else:
                return minValue(state, depth, agent, a, b)



        def maxValue(state, depth, agent, a, b):
            """
            #check base case
            if  depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), "nonextMove"
            """
            storeList = ["nothing", -float("inf")]

            nextmoves = state.getLegalActions(agent)
            
            #choose one of the best options
            for move in nextmoves:
            
                nowVal = updateFunction(state.generateSuccessor(agent, move), depth, agent+1, a, b)

                #handle different no. of actions
                immedVal = checker(nowVal)

                #deciding correct moves
                if immedVal > storeList[1]:
                    storeList = [move, immedVal]

                #a-b pruning
                if immedVal > b:
                    return [move, immedVal]
                a = max(a, immedVal)

                #print(storeList)

            return storeList

        def minValue(state, depth, agent, a, b):
            """
            #check base case
            if  depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), "nonextMove"
            """
            storeList = ["nothing", float("inf")]

            nextmoves = state.getLegalActions(agent)
            
            #choose one of the best options
            for move in nextmoves:
            
                nowVal = updateFunction(state.generateSuccessor(agent, move), depth, agent+1, a, b)

                #handle different no. of actions
                immedVal = checker(nowVal)

                #deciding correct moves
                if immedVal < storeList[1]:
                    storeList = [move, immedVal]

                #a-b pruning 
                if immedVal < a:
                    return [move, immedVal]
                b = min(b, immedVal)

                #print(storeList)

            return storeList

        def checker(nowVal):
            #one 
            if type(nowVal) is not list:
                return nowVal
            #more than one ->choose the first one out of list
            else:
                return nowVal[1]
        

        #init: a: -inf  b: +inf
        ansList = updateFunction(gameState, 0, 0, -float("inf"), float("inf"))
        return ansList[0]

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
        
        def updateFunction(state, depth, agent):

            #update depth, agent
            if agent >= state.getNumAgents():
                depth += 1
                agent = 0

            #Base case
            if (depth==self.depth or state.isWin() or state.isLose()):
                return self.evaluationFunction(state)

            #decide max or min function 
            if (agent == 0):
                return maxValue(state, depth, agent)
            else:
                return expectedValue(state, depth, agent)



        def maxValue(state, depth, agent):
            
            storeList = ["nothing", -float("inf")]

            nextmoves = state.getLegalActions(agent)

            #choose one of the best options
            for move in nextmoves:
            
                nowVal = updateFunction(state.generateSuccessor(agent, move), depth, agent+1)

                #handle different no. of actions
                immedVal = checker(nowVal)

                #deciding correct moves
                if immedVal > storeList[1]:
                    storeList = [move, immedVal]

                #print(storeList)

            return storeList

        def expectedValue(state, depth, agent):
            
            storeList = ["nothing", 0]

            nextmoves = state.getLegalActions(agent)

            #print(len(nextmoves))
            prob = 1.0/len(nextmoves)

            #choose one of the best options
            for move in nextmoves:
            
                nowVal = updateFunction(state.generateSuccessor(agent, move), depth, agent+1)

                #handle different no. of actions
                immedVal = checker(nowVal)

                #finding expected value
                #prob = 1/length of next moves(ghost)
                storeList[0] = move
                storeList[1] += immedVal * prob

                #print(storeList)

            return storeList

        def checker(nowVal):
            #one 
            if type(nowVal) is not list:
                return nowVal
            #more than one ->choose the first one out of list
            else:
                return nowVal[1]


        ansList = updateFunction(gameState, 0, 0)
        return ansList[0]


        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <Use the recipocal of distance of Pacman and food (as the only factor) to determine the moves>
    """
    "*** YOUR CODE HERE ***"

    Score = currentGameState.getScore() 
    #print(Score)
    
    #init Pacman position and food position
    PacPos = list(currentGameState.getPacmanPosition())
    foodPos = currentGameState.getFood().asList() 

    #create a list store distance between food and Pacman
    foodList = [] 
    for food in foodPos:
        Dist = manhattanDistance(food, PacPos)
        foodList.append(1/Dist)         #use recipocal of its value
    
    if not foodList:
        foodList.append(0)
    
    largestVal = max(foodList)
    #print(largestVal)
    
    return largestVal + Score


    util.raiseNotDefined()
    
# Abbreviation
better = betterEvaluationFunction

