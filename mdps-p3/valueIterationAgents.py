# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # for calculating value iteration we have this formula:
        #    V_k+1(s) = max_a ( sigma_s'( T(s,a,s')*[R(s,a,s') + gamma*V_k(s')] ) )
        # also instead of that we can use this formula:
        #    V_k+1(s) = max_a ( Q(s, a) )
        # and instead of calculating max on different possible action we can find policy according to current q values at first
        # then we use this formula:
        #    V_k+1(s) = Q(s, policy)
        for k in range(self.iterations):
            # for each state we find new value with value iteration and store it in new_values
            new_values = util.Counter()
            # in each iteration we do this calculations on all states so we need a loop
            all_states = self.mdp.getStates()
            for state in all_states:
                # only for terminal states we dont run value iteration algorithm
                if not self.mdp.isTerminal(state):
                    # first) we should find the best action according to current values 
                    policy = self.computeActionFromValues(state)
                    # second) from this values we can calculate 
                    newValue = self.computeQValueFromValues(state, policy)
                    # third) add this new value for this state to new_values
                    new_values[state] = newValue
            # update values of all state after iteration k
            self.values = new_values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # our formula for calculating Q value is :
                #QValue = sigma_s' ( T(s,a,s') [R(s,a,s') + gamma * V(s')])
        # so first we should find all possible transactions from current state:
        posssibleTransactions = self.mdp.getTransitionStatesAndProbs(state, action)
        # initialize QValue to 0
        QValue = 0
        # now according to formula we should find T(s,a,s') and R(s,a,s') and V(s')
        #   state = s
        #   next_state = s' 
        #   T = T(s,a,s')
        #   R = R(s,a,s')
        #   discount = gamma
        for next_state, T in posssibleTransactions:
            # calculate R(s,a,s')
            R = self.mdp.getReward(state, action, next_state)
            # calculate V(s')
            V_next_state = self.getValue(next_state)
            # find gamma value (discount factor)
            discount = self.discount
            # finally calculate QValue according to formula
            QValue += T * (R + discount * V_next_state)
        return QValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # according to above explanation we should check if we are in terminal state then return None
        if self.mdp.isTerminal(state):
            return None
        # according to below figure we should calculate QValue for current state and all possible actions(mabe some q aren`t accessible`)
        # ---------
        # | \ q1 / |
        # |q4 \/ q2|
        # |   /\   |
        # | / q3 \ |
        # ----------
        # then for finding policy or best action we have this formula:
        #    policy(s) = argmax_a (Qvalue(s,a))
        # so first we should find all possible actions in current state
        possible_actions = self.mdp.getPossibleActions(state)
        # with the help of util.counter we can create a dict of qvalues according to each action
        QValues = util.Counter()
        # then we can calculate QValue for each action with computeQValueFromValues() function
        for action in possible_actions:
            QValues[action] = self.computeQValueFromValues(state, action)

        policy = QValues.argMax()
        return policy

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)