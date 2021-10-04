import numpy as np
import random
from math import gcd

F = {0:0, 1:1}
L = {0:2, 1:1}

def Fibo(i):
    global F
    if i in F:
        return F[i]
    else:
        F[i] = Fibo(i-1) + Fibo(i-2)
        return F[i]


def Lucas(i):
    global L
    if i in L:
        return L[i]
    else:
        L[i] = Lucas(i-1) + Lucas(i-2)
        return L[i]

def const(a, s):
    u, v = Fibo(a), Lucas(a)
    r = (a+1) & 1
    k = u**4 - ((s**2)*(v - 1 + (-1)**r))**2
    return np.abs(k)

def D(a, s, n):
    u, v = Fibo(n), Fibo(n+a)
    return gcd(u+s, v+s)

def TheoremCheck(p, c):
    u, v = Fibo(p), Fibo(p + 1)
    return (u % c == 0 and v % c == 1)

def SmallestPeriodExample(a, s):
    start = D(a, s, 0)
    first = 1
    i = 1
    p, c = TheoremPeriod(a, s)
    while True:
        current = D(a, s, i)
        if current == start:
            first = i if first == 1 else first
            done = True
            for j in range(p):
                if D(a, s, j) != D(a, s, j + i):
                    done = False
                    break
            if done:
                return (i, TheoremCheck(i, c), p, c)
        i += first

def TheoremPeriod(a, s):
    c = const(a, s)
    p = 1
    u, v = Fibo(p), Fibo(p + 1)
    while p <= c**2:
        if(u % c == 0 and v % c == 1):
            return p, c
        u, v = v, u + v
        p += 1


def CheckInS(a, s):
    if (a, s) in {(1, 1), (1, -1), (3, 1), (3, -1)}:
        return False
    if a & 3 == 2:
        a >>= 1
        if (np.abs(s) == Fibo(a)):
            return False
    return True

if __name__ == "__main__":
    a, s = 1, 1
    count = 5
    while count > 0:
        if CheckInS(a, s):
            res = SmallestPeriodExample(a, s)
            if not res[1]:
                print(f"The theorem is not optimal for a = {a}, s = {s} with the smallest period p' = {res[0]} while p = {res[2]} and c = {res[3]}")
                count -= 1
            else:
                print(f"The theorem is optimal for a = {a}, s = {s} with the smallest period p = {res[0]} and c = {res[3]}")
        r = random.randint(0, 1)
        if r == 0:
            a += 1
        else:
            e = random.randint(0, 1)
            s = abs(s) + 1
            s *= (-1)**e
