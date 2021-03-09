import numpy as np

directions = {'left': '←', 
              'up': '↑',
              'right': '→', 
              'down': '↓'} 

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
            self.temp = sum([i * 0.25 for i in policy_vals])

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

def print_greedy_grid(grid):
    for i in range(len(grid)):
        grid_row = []
        for j in range(len(grid)):
            grid_square = grid[i][j]
            if (grid_square.end_state == True):
                grid_row.append(["."])
            else:
                surrounding_vals = []
                if (grid_square.left):
                    surrounding_vals.append(['left', grid_square.left.value])
                if (grid_square.right):
                    surrounding_vals.append(['right', grid_square.right.value])
                if (grid_square.up):
                    surrounding_vals.append(['up', grid_square.up.value])
                if (grid_square.down):
                    surrounding_vals.append(['down', grid_square.down.value])
                char_directions = [val[0] for val in surrounding_vals if val[1] >= max([item[1] for item in surrounding_vals])]
                grid_row.append([directions[direction] for direction in char_directions])
        print(grid_row)       
                
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
        print_greedy_grid(grid)
        grid_update(grid)
    

basic_gridworld(10000)