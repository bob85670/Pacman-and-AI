import mdp, util

from learningAgents import ValueEstimationAgent

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

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        for i in range(0, self.iterations):

            #get original new value and states
            newvalue = util.Counter()
            states = self.mdp.getStates()

            #iterate through each states
            for s in states:
                if self.mdp.isTerminal(s) or len(self.mdp.getPossibleActions(s))==0:
                    newvalue[s]=0
                    continue
                
                
                max_val = -99999

                #calcalute the q value
                for a in self.mdp.getPossibleActions(s):
                    Qval = self.getQValue(s,a)
                    
                    if Qval > max_val:
                        max_val = Qval

                #store the value as the next V value
                v_next = max_val
                newvalue[s] = v_next

            #update the self.values
            self.values = newvalue


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

        #get transition states 
        transstateandprob = self.mdp.getTransitionStatesAndProbs(state,action)
        Q_value = 0

        #calcalute q-value by transition state
        for s in transstateandprob:
            Reward = self.mdp.getReward(state, action, s[0])
            temp_Qval = s[1] * ( Reward + (self.discount * self.getValue(s[0])) )
            Q_value += temp_Qval

        return Q_value

        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        #"NONE" cases
        if self.mdp.isTerminal(state) or len(self.mdp.getPossibleActions(state))==0:
            return None

        max_val = -99999

        allStates = self.mdp.getPossibleActions(state)

        #calculate q values of each state
        for a in allStates:
            Qval = self.getQValue(state,a)

            #find the best move 
            if Qval > max_val:
                max_val = Qval
                move = a
        return move

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
