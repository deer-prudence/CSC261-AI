import numpy as np

class Gridspace:
    def __init__(self, value: float, punishment, end_state = False):
        self.value = value
        self.temp = value
        self.punishment = punishment
        self.end_state = end_state
        self.left, self.right, self.up, self.down = [None, None, None, None]

    def after_iteration(self):
        self.value = self.temp

    def update_value(self):
        if (self.end_state == False):
            if (self.left):
                left = self.punishment + self.left.value
            else: # return to current spot
                left = self.punishment + self.value
            if (self.right):
                right = self.punishment + self.right.value
            else: # return to current spot
                right = self.punishment + self.value
            if (self.up):
                up = self.punishment + self.up.value
            else: # return to current spot
                up = self.punishment + self.value
            if (self.down):
                down = self.punishment + self.down.value
            else: # return to current spot
                down = self.punishment + self.value
            policy_vals = [left, right, up, down]
            #print(policy_vals)
            max_vals = [i for i in policy_vals if i == max(policy_vals)]
            #print(max_vals)
            self.temp = sum([1/len(max_vals) * k for k in max_vals])
            #print(self.temp)

def make_grid(dimension):
    temp_arr = [[Gridspace(0, -1) for i in range(dimension)] for j in range(dimension)]
    grid_world = np.array(temp_arr)

    for i in range(dimension):
        for j in range(1, dimension):
            tile = grid_world[i][j]
            tile.left = grid_world[i][j - 1]
    
    for i in range(dimension):
        for j in range(0, dimension - 1):
            tile = grid_world[i][j]
            tile.right = grid_world[i][j + 1]

    for i in range(0, dimension - 1):
        for j in range(dimension):
            tile = grid_world[i][j]
            tile.down = grid_world[i + 1][j]
    
    for i in range(1, dimension):
        for j in range(dimension):
            tile = grid_world[i][j]
            tile.up = grid_world[i - 1][j]

    return grid_world

def print_grid(grid, dec):
    for i in range(len(grid)):
        arr = [round(grid[i][j].value, dec) for j in range(len(grid))]
        print(str(arr))
    print("\n")

def grid_update(grid):
    [[grid[i][j].update_value() for j in range(len(grid))] for i in range(len(grid))]
    [[grid[i][j].after_iteration() for j in range(len(grid))] for i in range(len(grid))]

def basic_gridworld(repetitions):
    grid = make_grid(4)
    grid[0][0].end_state = True
    grid[3][3].end_state = True
    for i in range(repetitions):
        print_grid(grid, 1)
        grid_update(grid)
    print_grid(grid, 1)
    

basic_gridworld()