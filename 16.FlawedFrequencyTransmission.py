import datetime
import math
import numpy as np
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''03081770884921959731165446850517'''
INPUT = '''59765216634952147735419588186168416807782379738264316903583191841332176615408501571822799985693486107923593120590306960233536388988005024546603711148197317530759761108192873368036493650979511670847453153419517502952341650871529652340965572616173116797325184487863348469473923502602634441664981644497228824291038379070674902022830063886132391030654984448597653164862228739130676400263409084489497532639289817792086185750575438406913771907404006452592544814929272796192646846314361074786728172308710864379023028807580948201199540396460310280533771566824603456581043215999473424395046570134221182852363891114374810263887875638355730605895695123598637121'''

def parse_input(input):
    return list(map(int,list(input)))

def phase(input_signal):
    base_pattern = [0, 1, 0, -1]
    output = []
    n = len(input_signal)
    for i in range(1, n + 1):
        #print(i)
        pattern = [val for val in base_pattern for _ in range(i)]
        pattern = pattern * math.ceil(n / len(pattern))
        if len(pattern) - 1 < n:
            pattern = pattern[1:] + pattern
        else:
            pattern = pattern[1:]
        out_digit = abs(np.dot(np.array(pattern[:n]), np.array(input_signal))) % 10
        output.append(out_digit)
    return output

def part1(input):
    signal = input.copy()
    for p in range(100):
        signal = phase(signal)
        # progress tracking
        if p%10  == 0:
            print('Phase {:,} done'.format(p+1))
    return ''.join(list(map(str, signal[:8])))

# Idea: in each phase
# - Last digit:         applied pattern = ...000001  => last digit never changes
# - 2nd last digit:     applied pattern = ...000011  => digit = last digit + 2nd last digit of previous phase
# - 3rd last digit:     applied pattern = ...000111  => digit = last digit + 2nd last + 3rd last of previous phase
# => 2nd half of the phase, pattern is only ...0000111...1  => last nth digit = sum(n digit of previous phase)
# Thanks to the 7-digit offset, the digits that need to be calculated are all in 2nd half 
# input: signal after skipping n digits according to message offset
def phase_offset(signal):
    output_signal = [signal[-1]]
    n = len(signal)
    for i in range(1,n):
        #print(output_signal[i-1], signal[-i-1], output_signal[i-1] + signal[-i-1])
        output_signal.append((output_signal[i-1] + signal[-i-1]) % 10)
    return list(reversed(output_signal))

def part2(input):
    signal = input * 10000
    offset = int(''.join(list(map(str,input[:7]))))
    signal = signal[offset:]
    print(len(signal))
    for p in range(100):
        signal = phase_offset(signal)
        # progress tracking
        if p%10  == 0:
            print('Phase {:,} done'.format(p+1))

    return ''.join(list(map(str, signal[:8])))

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
