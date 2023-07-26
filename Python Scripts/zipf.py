import math
import random

EULER = 0.5772156649


# returns n where the nth most common element is selected out of num_of_elements in a zipfy distribution
# n is always an integer between 0 and n-1 inclusively
# read more about zipf's law here:
# https://en.wikipedia.org/wiki/Zipf%27s_law
def zipfy_random(num_of_elements):
    rand = random.random() * triangular_number(num_of_elements)
    output = 0
    while triangular_number(output) < rand:
        output += 1
    output = num_of_elements - output
    return output


# defined as 1 + 2 + 3 + ... + n
# This calculation can be reduced to O(1) using formula from:
# https://en.wikipedia.org/wiki/Triangular_number
def triangular_number(n):
    return (n * n + n) / 2


# the nth harmonic number is defined as 1 + 1/2 + 1/3 + 1/4 + ... + 1/n
def harmonic_number(inp):
    if inp > 1000:
        return fast_harmonic_number(inp)
    else:
        return precise_harmonic_number(inp)


def fast_harmonic_number(inp):
    return math.log(inp) + EULER + (1 / (2 * inp)) - (1 / (12 * inp * inp))


# approximates harmonic number inp using formula from this webpage:
# https://www.johndcook.com/blog/2017/04/18/computing-harmonic-numbers/
# this formula has 11 digits of accuracy at fastHarmonicNumber(1000)
def precise_harmonic_number(inp):
    out = 0
    for i in range(1, inp):
        out += (1 / i)
    return out
