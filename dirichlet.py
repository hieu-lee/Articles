import math

def fractional(n):
    return n - int(n)

def seq(a, i):
    if i == 1:
        return fractional(a)
    else:
        res = fractional(a)
        index = 1
        while index < i:
            res = (int(1/res) + 1) * res - 1
            index += 1
        return res


def get_small_term(a, epsilon):
    res = fractional(a)
    index = 1
    while res >= epsilon:
        res = (int(1/res) + 1) * res - 1
        index += 1
    return index

def get_small_number(a, epsilon):
    res = fractional(a)
    n = 1
    index = 1
    while res >= epsilon:
        n *= (int(1/res) + 1)
        res = (int(1/res) + 1) * res - 1
        index += 1
    return (res, n, index)

def kronecker(a, b, epsilon):
    # a is an irrational number, b in (0,1) and 0 < epsilon < min{b, 1 - b}
    # Find n such that |{na} - b| < epsilon.
    m = min(b, 1-b)
    epsilon = m/2 if epsilon >= m else epsilon
    res = get_small_number(a, 2*epsilon)
    s = int((b - epsilon)/res[0])
    return res[1] * (s + 1)

def get_Q(a, epsilon):
    res = fractional(a)
    n = 1
    index = 1
    while res*(int(1/res)) <= 1 - epsilon:
        n *= (int(1/res) + 1)
        res = (int(1/res) + 1) * res - 1
        index += 1
    n *= (int(1/res))
    return n

def dirichlet(a, k, epsilon):
    # a is an array of length k, epsilon > 0
    # a contains k irrational numbers
    # Find positive integer n and an array b of length k containing 0 and 1 such that
    # |{na[i]} - b[i]| < epsilon for all i.
    if k == 1:
        return (kronecker(a[0], 1-epsilon/2, epsilon/2), [1])
    else:
        if epsilon > 0.5:
            b = [0 if fractional(a[i]) < 0.5 else 1 for i in range(k)]
            return (1, b)
        else:
            m = int(1/epsilon)
            n, b = dirichlet(a, k-1, epsilon/((m+1)**m))
            c = fractional(a[k-1]*n)
            if c < epsilon:
                b.append(0)
                return (n, b)
            elif c > 1 - epsilon:
                b.append(1)
                return (n, b)
            else:
                _, P, index = get_small_number(c, epsilon)
                index -= 1
                if index <= m:
                    b.append(0)
                    return (P*n, b)
                else:
                    b.append(1)
                    Q = get_Q(c, epsilon)
                    return (Q*n, b)
