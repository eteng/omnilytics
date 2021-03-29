import random
import string
import sys


def gen_alpha_str():
    # generate alphabetical string
    length = random.randint(1, 20)
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))
    
def gen_alpha_numberic():
    # generate alphanumerics
    length = random.randint(1, 20)
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def gen_integer_only():
    # generate integer
    return random.randint(0, sys.maxsize)

def gen_real_number():
    # generate real number
    return random.uniform(75.5, 125.5,)


def gen_all_rand():
    choices = [gen_alpha_str, gen_alpha_numberic,gen_integer_only,gen_real_number]
    rand_type = random.choice(choices)
    return rand_type()