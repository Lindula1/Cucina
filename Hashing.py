import math
from mpmath import mp

key = 29327
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
    h = (((int(h) // math.factorial(len(s)))) % (int(d) // math.factorial(len(s)))) % key + 1

    pinum = pi[h:h+69]
    nums = int("".join(pinum))
    digits = list(Digitize(nums, 26))
    hashed = ""
    for num in digits:
        hashed += chr(num + 64)

    return hashed

if __name__ == "__main__":
    tstWrds = ["password", "fortnite420", "green", "hotdog69"]
    for wrd in tstWrds:
        h = HashingFunc(wrd)
        print(f"'{wrd}' Hashed: {h}")