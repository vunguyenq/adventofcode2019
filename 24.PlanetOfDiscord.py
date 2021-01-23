import datetime
import numpy as np

exec_part = 1 # which part to execute
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

def part2(input):
    result = 0
    return result

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