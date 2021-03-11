import numpy as np
from numpy import random as rn
import matplotlib.pyplot as pp

directions = {'left': '←', 
              'up': '↑',
              'right': '→', 
              'down': '↓'} 

class Agent:
    def __init__(self, mdp, gamma, epsilon, alpha):
        self.mdp = mdp
        self.gamma = gamma
        self.epsilon = epsilon
        self.alpha = alpha
        self.Q = {}

    def policy(self, s): # Good
        if s not in self.Q: # initialize if null
            self.Q[s] = {'←': 0,
                         '↑': 0,
                         '→': 0,
                         '↓': 0}
        if rn.rand() <= self.epsilon: # higher epsilon means more random
            return list(self.Q[s].keys())[rn.choice(4)] # pick random route
        return max(self.Q[s], key=self.Q[s].get) # otherwise pick max route
    
    def train_Q(self, episodes, epsilon, alpha):
        t = 1 # we count time steps for each simulation

        episode_reward = []

        self.epsilon = epsilon
        self.alpha = alpha

        for i in range(episodes):
            
            reward = 0
            
            s = self.mdp.s # where MDP = (punishment, [start-coord, end-coord], width, height, terminal-coord)

            
            while s not in self.mdp.terminal:                
                if epsilon == -1:
                    self.epsilon = 1 / t
                if alpha == -1:
                    self.alpha = 1 / t
                if i > 400:
                    self.epsilon = 0


                a = self.policy(s) # choose between maximization policy and random policy
                self.mdp.evolve(a) # change the environment based on the action
                self.policy(self.mdp.s)
                # mdp = markov decision process: self.mdp.R[self.mdp.s] gets reward based on update environment and chosen action
                # self.mdp.s = next state; max(self.Q[self.mdp.s]) assumed our next policy is maximizing
                
                self.Q[s][a] += self.alpha * (self.mdp.R[self.mdp.s] + self.gamma * self.Q[self.mdp.s][max(self.Q[self.mdp.s])] # Target
                                            - self.Q[s][a])
                # update current state according to chosen action

                reward += self.mdp.R[self.mdp.s]
                s = self.mdp.s # Update tracker for current state
            t += 1
            
            self.mdp.s = (3,0) # Reset to initial state

            episode_reward.append(reward)

            
        return episode_reward


class MDP:
    def __init__(self, defaultR, terminal, h, w, initialS):
        self.h = h
        self.w = w
        self.R = defaultR*np.ones((h,w))
        self.terminal = terminal
        self.s = initialS # (x, y) pair

        for s in terminal:
            self.R[s] = 1
    
    def evolve(self, a):
        y,x = self.s
        if a == '←':
            x = x - 1 if x > 0 else x
        elif a == '→':
            x = x + 1 if x < self.w - 1 else x
        elif a == '↑':
            y = y - 1 if y > 0 else y
        elif a == '↓':
            y = y + 1 if y < self.h - 1 else y
        self.s = (y,x)
         
def get_gridworld():
    gridworld = np.empty(16).reshape((4, 4))
    gridworld.fill(-1)
    gridworld[0][0] = 0
    gridworld[3][3] = 0
    return gridworld

def simulation(episodes, learning_rate, exploration_rate):
    mdp = MDP(-1, [(0,0),(3,3)], 4, 4, (3,0))
    agent = Agent(mdp, 0.9, 0.9, 0.9)
    return agent.train_Q(episodes, learning_rate, exploration_rate)
    

def main():
    # 5 simulations, n episodes
    episodes = 300
    sim1_rewards = np.zeros((episodes,1))
    for i in range(5):
        sim1_rewards += np.reshape(simulation(episodes, 0.1, 0.25), (episodes,1)) # first_sim
    sim1_rewards /= 5
    pp.plot(np.arange(episodes), sim1_rewards)
    pp.xlabel("Episodes")
    pp.ylabel("Average Reward")
    pp.ylim(-20, 5)
    pp.hlines(-1, 0, episodes, colors=["red"], linestyles="dashed")
    pp.title("Experiment I; γ=0.9, α=0.1, ε=0.25")
    pp.show()
    
    sim2_rewards = np.zeros((episodes,1))
    for i in range(5):
        sim2_rewards += np.reshape(simulation(episodes, -1, -1), (episodes,1)) # first_sim
    sim2_rewards /= 5
    pp.plot(np.arange(episodes), sim2_rewards)
    pp.xlabel("Episodes")
    pp.ylabel("Average Reward")
    pp.ylim(-20, 5)
    pp.hlines(-1, 0, episodes, colors=["red"], linestyles="dashed")
    pp.title("Experiment II; γ=0.9, α=1/T, ε=1/T")
    pp.show()
    # second_sim = [0.9, 1/T, 1/T]

    sim3_rewards = np.zeros((episodes,1))
    for i in range(5):
        sim3_rewards += np.reshape(simulation(episodes, 0.1, -1), (episodes,1)) # first_sim
    sim3_rewards /= 5
    pp.plot(np.arange(episodes), sim3_rewards)
    pp.xlabel("Episodes")
    pp.ylabel("Average Reward")
    pp.ylim(-20, 5)
    pp.hlines(-1, 0, episodes, colors=["red"], linestyles="dashed")
    pp.title("Experiment III; γ=0.9, α=0.1, ε=1/T")
    pp.show()
    # third_sim = [0.9, 0.1, 1/T]
    return

main()