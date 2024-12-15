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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        "*** YOUR CODE HERE ***"
        Food=newFood.asList()
        gPos=successorGameState.getGhostPositions()                         
        FoodDist=[]                                                         
        GhostDist=[]

        for food in Food:
            FoodDist.append(manhattanDistance(food,newPos))
        for ghost in gPos:
            GhostDist.append(manhattanDistance(ghost,newPos))

        if currentGameState.getPacmanPosition()==newPos:
            return(-(float("inf")))

        for dist in GhostDist:                                              
            if dist<2:
                return (-(float("inf")))                                    
        if len(FoodDist)==0:                                                
            return float("inf")                                             
                                                                            
        return 1000/sum(FoodDist) +10000/len(FoodDist)

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
       ##Q2 OG code: util.raiseNotDefined()
        def max_value(gameState, depth):
            Actions=gameState.getLegalActions(0)
            if len(Actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:             
                return(self.evaluationFunction(gameState),None)
            w=-(float("inf"))                                                                               
            Act=None
            for action in Actions:                                                                          
                sucsValue=min_value(gameState.generateSuccessor(0,action),1,depth)                          
                sucsValue=sucsValue[0]                                                                      
                if(sucsValue>w):                                                                            
                    w,Act=sucsValue,action
            return(w,Act)
        def min_value(gameState, agentID, depth):
            Actions=gameState.getLegalActions(agentID)
            if len(Actions) == 0:
                return(self.evaluationFunction(gameState),None)
            l=float("inf")                                                                                  
            Act=None
            for action in Actions:
                if(agentID==gameState.getNumAgents() -1):
                    sucsValue=max_value(gameState.generateSuccessor(agentID,action),depth + 1)
                else:
                    sucsValue=min_value(gameState.generateSuccessor(agentID,action),agentID+1,depth)        
                sucsValue=sucsValue[0]
                if(sucsValue<l):
                    l,Act=sucsValue,action
            return(l,Act)
        max_value=max_value(gameState,0)[1]
        return max_value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState,depth,a,b):
            Actions = gameState.getLegalActions(0) # Get actions of pacman
            if len(Actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:
                return (self.evaluationFunction(gameState), None)

            w=-(float("inf"))
            Act=None
                                                                                                            
                                                                                                            
            for action in Actions:
                sucsValue=min_value(gameState.generateSuccessor(0,action),1,depth,a,b)
                sucsValue=sucsValue[0]
                if w<sucsValue:
                    w,Act=sucsValue,action
                if w>b:
                    return (w,Act)
                a=max(a,w)
            return (w,Act)

        def min_value(gameState,agentID,depth,a,b):
            " Cases checking "
            Actions=gameState.getLegalActions(agentID) 
            if len(Actions) == 0:
                return (self.evaluationFunction(gameState),None)
                                                                                                            
                                                                                                            
                                                                                                            
            l = float("inf")
            Act = None
            for action in Actions:
                if (agentID == gameState.getNumAgents() - 1):
                    sucsValue = max_value(gameState.generateSuccessor(agentID,action),depth + 1,a,b)
                else:
                    sucsValue = min_value(gameState.generateSuccessor(agentID,action),agentID + 1,depth,a,b)
                sucsValue=sucsValue[0]
                if (sucsValue<l):
                    l,Act=sucsValue,action

                if (l<a):
                    return (l,Act)

                b=min(b,l)

            return(l,Act)                                                                                      

        a=-(float("inf"))
        b=float("inf")
        max_value=max_value(gameState,0,a,b)[1]
        return max_value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState,depth):
            Actions=gameState.getLegalActions(0)
            if len(Actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:
                return (self.evaluationFunction(gameState),None) 

            w=-(float("inf"))
            Act=None

            for action in Actions:
                sucsValue=exp_value(gameState.generateSuccessor(0,action),1,depth)
                sucsValue=sucsValue[0]
                if(w<sucsValue):
                    w,Act=sucsValue,action                                              
                                                                                                    
                            
            return(w,Act)

        def exp_value(gameState,agentID,depth):
            Actions=gameState.getLegalActions(agentID)
            if len(Actions)==0:
                return (self.evaluationFunction(gameState),None)

            l=0
            Act=None
            for action in Actions:
                if(agentID==gameState.getNumAgents() -1):
                    sucsValue=max_value(gameState.generateSuccessor(agentID,action),depth+1)
                else:
                    sucsValue=exp_value(gameState.generateSuccessor(agentID,action),agentID+1,depth)
                sucsValue=sucsValue[0]
                prob=sucsValue/len(Actions)
                l+=prob
            return(l,Act)

        max_value=max_value(gameState,0)[1]
        return max_value

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <This evaluation function considers the Manhattan distance between Pac-Man and the ghosts, the Manhattan distance between Pac-Man and the capsules, and the current game score. It adjusts the score by subtracting the distance to the ghosts and adding the distance to the capsules.>
    """
    "*** YOUR CODE HERE ***"
    # retrieve all the info
    pacPosition=currentGameState.getPacmanPosition()                                                     
    gList=currentGameState.getGhostStates()                                                              
    Food=currentGameState.getFood()
    Capsules=currentGameState.getCapsules()
    Score = currentGameState.getScore()
    currentScore = 0

    if(len(Capsules) != 0):
        for c in Capsules:
            c_dis = min([manhattanDistance(c, pacPosition)])
            if c_dis == 0 :
                c_score = float(1)/c_dis
            else:
                c_score = -100

    for gh in gList:
        gh_x = (gh.getPosition()[0])
        gh_y = (gh.getPosition()[1])
        gh_pos = gh_x,gh_y
        gh_dis = manhattanDistance(pacPosition, gh_pos)

    return Score  - (1.0/1+gh_dis)  + (1.0/1+currentScore)


# Abbreviation
better = betterEvaluationFunction
