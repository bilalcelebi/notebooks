import math

def get_factoriel(n):

    return int(math.factorial(int(n)))


def calculate_permutations(n,r):

    n_factor = get_factoriel(n)
    n_minus_r_factor = get_factoriel(int(n-r))

    result = n_factor / n_minus_r_factor

    return result


def calculate_combinations(n, r):

    n_factor = get_factoriel(n)
    r_factor = get_factoriel(r)
    n_minus_r_factor = get_factoriel(int(n-r))

    result = n_factor / (r_factor * n_minus_r_factor)

    return result


if __name__ == '__main__':

    n = int(input("Put N number : "))
    r = int(input("Put R number : "))
    
    permutations = calculate_permutations(n, r)
    combinations = calculate_combinations(n, r)

    print(f'Permutations : {permutations}\nCombinations : {combinations}')
