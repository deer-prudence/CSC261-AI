import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class State:
    def __init__(self, w, h, default_reward):
        self.world = np.reshape(np.array([GridSpace(default_reward, x, y) for x in range(w) for y in range(h)]), (h, w))
        self.w = w
        self.h = h

    def get_square(self, x, y):
        return self.world[y,x]

class Agent:
    def __init__(self, discount):
        self.discount = discount
    

class MDP:
    def __init__(self, s0, default_reward):
        self.pos = (0,0)
        self.state = s0
        
        self.A = '←↑→↓.'

    def T(s,a):
        squares = {'←': (pos[0], pos[1] - 1), 
                   '↑': (pos[0] - 1, pos[1]),
                   '→': (pos[0], pos[1] + 1), 
                   '↓': (pos[0] - 1, pos[1]), 
                   '.': (pos[0], pos[1])}
        square = squares[a]
        state_copy = self.state.copy()

        update = state.get_square(square[0],square[1]).on_move(a) # (coord to change, type of space to change to)
        
        self.state_copy.world[agent_position] = GridSpace(default_reward, agent_position[0], agent_position[1])
        self.state_copy.world[update[0]] = update[1]

        return (state_copy, square)
            

# ideas:
### crate the agent pushes around
### wall that goes up and down (in a pattern)
### 
class GridSpace:
    def __init__(self, reward, x, y):
        self.reward = reward
        self.x = x
        self.y = y

    def on_move(self, direction):
        return ((self.x, self.y), self)        

class Crate(GridSpace):
    def __init__(self, reward, x, y):
        super(reward, x, y)
        self.squares = {'←': (x, y - 1), 
                        '↑': (x - 1, y),
                        '→': (x, y + 1), 
                        '↓': (x - 1, y), 
                        '.': (x, y)}

    def on_move(self, direction):
        coord = self.squares[direction]
        return (coord, Crate(0, coord[0], coord[1]))

class Button(GridSpace):
    def __init__(self, reward, x, y, p):
        super(reward, x, y)
        self.p_coord = (p.x, p.y)
    
    def on_move(self, direction):
        return (p_coord, GridSpace(default_reward, p_coord[0], p_coord[1])) # make default_reward global?

    
    
