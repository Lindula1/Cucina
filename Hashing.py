import math
from mpmath import mp

key = 58231
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
        h = key - (ord(entry[0]) + ord(entry[-1]) + ord(entry[1]))

    pinum = pi[h:h+65]
    nums = int("".join(pinum))
    digits = list(Digitize(nums, 26))
    hashed = ""
    for num in digits:
        hashed += chr(abs(num - 101))

    return hashed

if __name__ == "__main__":
    tstWrds = ["password", "fortnite420", "green", "hotdog69", "hotdog23", "h", "ho"]
    for wrd in tstWrds:
        h = HashingFunc(wrd)
        print(f"'{wrd}' Hashed: {h}")