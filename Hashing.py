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
        h = key - (ord(entry[0]))

    pinum = pi[h:h+65]
    nums = int("".join(pinum))
    digits = list(Digitize(nums, 26))
    hashed = ""
    for num in digits:
        hashed += chr(abs(num - 88))

    return hashed

if __name__ == "__main__":
    tstWrds = ["password", "fortnite420", "green", "hotdog69", "hotdog23", "Diplo", "ho", "the sly fox jumped over the lazy dog", "the sly fox jumped over the lanky dog", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam posuere libero dolor, quis placerat lectus sagittis at. Fusce sed elit sem. Nunc in placerat velit. Vivamus eu ex rhoncus, sollicitudin odio ut, scelerisque arcu. Aliquam ornare blandit magna sed venenatis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse varius neque at erat vehicula, in malesuada sapien facilisis. Etiam cursus quam eget arcu tristique, ac ultricies elit fringilla. Aliquam quis tincidunt libero. Nulla eget efficitur odio. Sed congue dictum volutpat. Suspendisse potenti. Praesent pretium scelerisque euismod. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam posuere libero dolor, quis placerat lectus sagittis at. Fusce sed elit sem. Nunc in placerat velit. Vivamus eu ex rhoncus, sollicitudin odio ut, scelerisque arcu. Aliquam ornare blandit magna sed venenatis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse varius neque at erat vehicula, in malesuada sapien facilisis. Etiam cursus quam eget arcu tristique, ac ultricies elit fringilla. Aliquam quis tincidunt libero. Nulla eget efficitur odio. Sed congue dictum volutpat. Suspendisse potenti. Praesent pretium scelerisque euismod. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas"]
    for wrd in tstWrds:
        h = HashingFunc(wrd)
        print(f"'{wrd}' Hashed: {h}")