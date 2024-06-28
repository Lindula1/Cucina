import math
from mpmath import mp
import string
import random
from timeit import repeat

key = 58231
seed = 161803398874989484820458683436563811772030917980576286213544862270526046281890
mp.dps = key + 69
pi = list(str(mp.pi).replace(".",""))

def Digitize(n, base=10):
    if n == 0:
        yield 0
    while n:
        n, d = divmod(n, base)
        yield d

def HashingFunc(entry):
    s = entry.encode("utf-8").hex()
    d = ""
    for i in entry:
        d += str(ord(i))
    h = []
    for c in s:
        h.append(str(ord(c)))
    h = "".join(h)
    try:
        h = ((int(h) * math.factorial(len(s))) % key) + 1
    except ZeroDivisionError:
        print("FATAL ERROR. HOW?")
        h = key - (ord(entry[0]))

    pinum = pi[h:h+65]
    nums = int("".join(pinum))
    digits = list(Digitize(nums, 26))
    hashed = ""
    for num in digits:
        hashed += chr(abs(num - 88))

    return hashed

def HashinFunc2(entry):
    d = ""
    for i in entry:
        d += str(ord(i))
    d = int(d)
    pinum = pi[d % key:(d % key)+65]
    s = int("".join(pinum))
    print(s)
    print(d)
    print(s*d)
    print(seed)
    nums = int(d * s) % seed
    digits = list(Digitize(nums, 52))
    hashed = ""
    for num in digits:
        if num < 26:
            hashed += chr(abs(num - 88))
        elif num > 26:
            hashed += chr(abs((num - 26) - 123))
    return hashed

if __name__ == "__main__":
    result = []
    tstWrds = []
    for i in range(2400):
        tstWrds.append(''.join(random.choices(string.ascii_letters, k=random.randint(2,20))))
    for i in tstWrds:
            num = tstWrds.count(i)
            result.append([i,num])
            if num > 1:
                print(f"{i} has {num} repeats.")
    bank = []
    c = 0
    for wrd in tstWrds:
        h = HashinFunc2(wrd)
        print(len(h))
        bank.append(h)
    for i in bank:
        num = bank.count(i)
        if num > 1:
            for l in range(len(bank)):
                if i == bank[l]:
                    print(f"{tstWrds[l]} {i} has {num} repeats.")
        result[c] = [result[c],["hashed",num]]
        c += 1

    tstWrds = ["password", "fortnite420", "green", "hotdog69", "hotdog23", "Diplo", "ho", "the sly fox jumped over the lazy dog", "the sly fox jumped over the lanky dog","l","m"]
    for wrd in tstWrds:
        h = HashinFunc2(wrd)
        print(f"'{wrd}' Hashed: {h}")