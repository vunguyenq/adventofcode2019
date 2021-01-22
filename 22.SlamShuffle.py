import datetime
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
INPUT_TEST = '''deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1'''
INPUT = '''deal with increment 31
deal into new stack
cut -7558
deal with increment 49
cut 194
deal with increment 23
cut -4891
deal with increment 53
cut 5938
deal with increment 61
cut 7454
deal into new stack
deal with increment 31
cut 3138
deal with increment 53
cut 3553
deal with increment 61
cut -5824
deal with increment 42
cut -889
deal with increment 34
cut 7128
deal with increment 42
cut -9003
deal with increment 75
cut 13
deal with increment 75
cut -3065
deal with increment 74
cut -8156
deal with increment 39
cut 4242
deal with increment 24
cut -405
deal with increment 27
cut 6273
deal with increment 19
cut -9826
deal with increment 58
deal into new stack
cut -6927
deal with increment 65
cut -9906
deal with increment 31
deal into new stack
deal with increment 42
deal into new stack
deal with increment 39
cut -4271
deal into new stack
deal with increment 32
cut -8799
deal with increment 69
cut 2277
deal with increment 55
cut 2871
deal with increment 54
cut -2118
deal with increment 15
cut 1529
deal with increment 57
cut -4745
deal with increment 23
cut -5959
deal with increment 58
deal into new stack
deal with increment 48
deal into new stack
cut 2501
deal into new stack
deal with increment 42
deal into new stack
cut 831
deal with increment 74
cut -3119
deal with increment 33
cut 967
deal with increment 69
cut 9191
deal with increment 9
cut 5489
deal with increment 62
cut -9107
deal with increment 14
cut -7717
deal with increment 56
cut 7900
deal with increment 49
cut 631
deal with increment 14
deal into new stack
deal with increment 58
cut -9978
deal with increment 48
deal into new stack
deal with increment 66
cut -1554
deal into new stack
cut 897
deal with increment 36'''

def parse_input(input):
    actions = []
    for row in input.split('\n'):
        last_word = row.split(' ')[-1]
        if(last_word == 'stack'):
            actions.append((row, 0))
        else:
            actions.append((row[:-len(last_word)-1],int(last_word)))
    return actions

def part1(input):
    n_cards = 10007
    deck = list(range(n_cards))
    #input = [('deal with increment', 3)]
    for action, val in input:
        if action == 'deal into new stack':
            deck = list(reversed(deck))
        elif action == 'deal with increment':
            new_deck = deck.copy()
            for i in range(n_cards):
                new_deck[i * val % n_cards] = deck[i]
            deck = new_deck
        else: # cut
            deck = deck[val:] + deck[:val]
    return deck.index(2019)

# https://codeforces.com/blog/entry/72593
# All shuffling techniques can be rewritten in a form of f(x) = ax+b (mod m)  ; m is deck size, card at position x is moved to f(x)
#   * "deal into new stack": f(x)=−x−1 (mod m), so a=−1,b=−1
#   * "cut n": f(x)=x−n (mod m), so a=1,b=−n 
#   * "deal with increment n": f(x)=nx (mod m), so a=n,b=0
# Let f1(x) = a1.x + b1 (mod m) ; f2(x) = a2.x + b2 (mod m) and so on
#   => f2(f1(x)) = a2(a1.x + b1) + b2 (mod m) = a1a2.x + b1a2 + b2 (mod m)                  (shuffle technique f1, then f2)
#   => f3(f2(f1(x))) = a3(a1a2.x + b1a2 + b2) + b3 = a1a2a3.x + b1a2a3 + b2a3 + b3      (shuffle technique f1, then f2, then f3)
# After (all transformation steps) * (k times): F(x) = a.x + b (mod m). Invert the function to get which card is at position x
def part2(input):
    m = 119315717514047
    k = 101741582076661
    x = 2020

    # Grouping all transformation steps (f1(f2(f3(...(fn(x)))))) into a single transformation f(x) = a.x + b (mod m)
    a, b = 1, 0
    for action, n in input:
        if action == 'deal into new stack':
            a1 = b1 = -1
        elif action == 'deal with increment':
            a1, b1 = n, 0
        else: # cut
            a1, b1 = 1, -n
        a = (a * a1) 
        b = (b * a1 + b1) 

    # Validate a, b by applying this apporach to part 1
    card, deck_size = 2019, 10007
    print('Validate Part 1 result with modular arithmetic approach: {}'.format((a * card + b) % deck_size))
    
    # Invert function: https://www.reddit.com/r/adventofcode/comments/jbu3ec/2019_day_22_a_thank_you_for_a_fun_mathy_puzzle/
    inv_a = pow(a, m - 2, m)
    inv_a_to_k = pow(inv_a, k, m)
    coef = ((inv_a_to_k - 1) * pow(inv_a - 1, m - 2, m) - 1) % m
    return ((x - b) * inv_a_to_k - b * coef) % m

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