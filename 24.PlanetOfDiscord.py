import datetime
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''....#
#..#.
#..##
..#..
#....'''
INPUT = '''#..#.
.....
.#..#
.....
#.#..'''

def parse_input(input):
    return np.array(list(map(int,input.replace('#','1').replace('.','0').replace('\n','')))).reshape(5,5)

# Convert list of bits [1,0,0,1,...] to int by shifting bits
def bit_list_to_int(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out

def count_adjacent_bugs(grid, coor):
    r,c = coor
    nr,nc = grid.shape
    bugs = 0
    for ar,ac in [(r+1,c),(r,c+1),(r-1,c),(r,c-1)]:
        if(ar < 0 or ac < 0 or ar >= nr or ac >= nc):
            continue
        bugs += grid[ar][ac]
    return bugs

def part1(input):
    grid = input.copy()
    grid_size = grid.shape
    previous_grids = set()
    minute = 0
    while(True):
        # Check if current grid state was seen before
        grid_int_bits = bit_list_to_int(list(grid.flatten()))
        if grid_int_bits in previous_grids:
            break
        
        # If not seen before, update grid state at current minute
        previous_grids.add(grid_int_bits)
        new_grid = grid.copy()
        for i in range(grid_size[0]):
            for j in range(grid_size[1]):
                val = grid[i][j]
                adjacent_bugs = count_adjacent_bugs(grid, (i,j))
                if val == 1:
                    new_grid[i][j] = 1 if adjacent_bugs == 1 else 0
                else:
                    new_grid[i][j] = 1 if adjacent_bugs == 1 or adjacent_bugs == 2 else 0
        grid = new_grid
        minute += 1
    print('Found repeated layout at minute {}'.format(minute))
    result = 0
    for i, d in enumerate(list(grid.flatten())):
        result += d*(2**i)
    return result

# Find adjacent tile of a given tile in a 3-D recursive space
def find_ajacents(coor):
    r, c, l = coor # row, col, layer
    adjacents = []
    for ar,ac in [(r+1,c),(r,c+1),(r-1,c),(r,c-1)]:
        # adjacents in the same layer
        if(ar,ac) == (2,2) or ar < 0 or ac < 0 or ar > 4 or ac > 4: pass
        else: adjacents.append((ar, ac, l))
        
        # adjacents in outer layer
        if ar < 0: adjacents.append((1, 2, l-1))
        if ar > 4: adjacents.append((3, 2, l-1))
        if ac < 0: adjacents.append((2, 1, l-1))
        if ac > 4: adjacents.append((2, 3, l-1))
        
        # adjacents in inner layers:
        if(ar, ac) == (2,2):
            if (r,c) == (1,2): adjacents = adjacents + [(0, i, l+1) for i in range(5)]
            if (r,c) == (3,2): adjacents = adjacents + [(4, i, l+1) for i in range(5)]
            if (r,c) == (2,1): adjacents = adjacents + [(i, 0, l+1) for i in range(5)]
            if (r,c) == (2,3): adjacents = adjacents + [(i, 4, l+1) for i in range(5)]
    return adjacents

def part2(input):
    first_layer = input.copy()
    # Initialize (n+1)*2 empty recursive layers (n+1 inner and n+1 outer of the given layers)
    empty_layout = np.zeros(25).reshape(5,5).astype(int)
    n_layers = 200
    space = [empty_layout.copy() for _ in range(n_layers * 2 + 3)]
    space[n_layers] = first_layer
    
    # run N minutes
    N_minutes = 200
    for minute in range(N_minutes):
        layers = list(range(n_layers-minute-1, n_layers+minute + 2)) # in a minute, bugs spread to maximum +-1 layers => at minute = 1,2,3, scan only (minute * 2 + 1) layers
        new_layers = []
        for l in layers:
            layer = space[l]
            new_layer = layer.copy()
            for r in range(5):
                for c in range(5):
                    if (r,c) == (2,2):
                        continue
                    val = layer[r][c]
                    bugs = 0
                    adjacents = find_ajacents((r,c,l))
                    for nr, nc, nl in adjacents:
                        bugs += space[nl][nr][nc]
                    if val == 1:
                        new_layer[r][c] = 1 if bugs == 1 else 0
                    else:
                        new_layer[r][c] = 1 if bugs == 1 or bugs == 2 else 0
            new_layers.append(new_layer)
        for i, l in enumerate(layers):
            space[l] = new_layers[i]

    bug_count = 0
    for l in layers:
        bug_count += np.sum(space[l])
    return bug_count

if __name__ == "__main__":
    if(exec_test_case == 1):
        input = INPUT_TEST
    else:
        input = INPUT
    input = parse_input(input)

    start_time = datetime.datetime.now() 
    if (exec_part == 1):
        result = part1(input)
    else:
        result = part2(input)
    end_time = datetime.datetime.now() 
    print('Part {} time: {}'.format(exec_part, end_time - start_time))
    print('Part {} answer: {}'.format(exec_part, result))