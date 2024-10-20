import collections
from itertools import combinations
from typing import List, Set
import random
import time
import math
import matplotlib.pyplot as plt
from random import randrange



original_length = []
critical_length = []
class Simplex:
    def __init__(self, obj: str):
        self.obj = str("".join(sorted(obj)))

    def __repr__(self):
        return self.obj

    def __str__(self):
        return self.obj

    def __hash__(self):
        return hash(self.obj)

    def __eq__(self, other: 'Simplex'):
        if isinstance(other, Simplex):
            return set(self.obj) == set(other.obj)
        return False

    def __sub__(self, other: 'Simplex'):
        r = "".join(list(set(self.obj) - set(other.obj)))
        return Simplex(r)

    def __len__(self):
        return len(self.obj)


def join(lst: List['Simplex']):
    r = "".join([s.obj for s in lst])
    return Simplex(r)


a, b, c, d = Simplex("a"), Simplex("b"), Simplex("c"), Simplex("d")
d0s = {a, b, c, d}
d1s = {join(list(comb)) for comb in combinations(d0s, 2)} - {join([a, d])}
d2s = {join([a, b, c])}

k = d0s | d1s | d2s  # union


def random_generator(k: int, d: int = 3):
    # k is number of d0 simplex
    if k == 0:
        return {}
    d0s = {Simplex(f"{i}") for i in range(k)}
    ds = [d0s]
    for r in range(1, d):
        dis = set()
        for comb in combinations(ds[-1], r+1):
            if len(join(list(comb))) == r+1:
                s = join(list(comb))
                dis.add(s)
        # dis = {join(list(comb)) for comb in combinations(ds[-1], r+1) if len(join(list(comb))) == r+1}
        if len(dis) > 0:
            removed_number = randrange(len(dis))
            dis -= set(random.choices((list(dis)), k=removed_number))
        ds.append(dis)
    return ds


# Make relationship map
# ds = [d0s, d1s, d2s]
# ds = random_generator(3)
# rdict_p_ = collections.defaultdict(set)
# rdict_m_ = collections.defaultdict(set)
# for i in range(len(ds)):
#     for e in ds[i]:
#         # high-level dimension
#         if i < len(ds) - 1:
#             rdict_p_[e] = {eh for eh in ds[i + 1] if len(eh - e) == 1}
#         # low-level dimension
#         if i > 0:
#             rdict_m_[e] = {el for el in ds[i - 1] if len(e - el) == 1}

def simplex_argmax(lst, dict):
    curr_cnt, curr_e = -1, None
    for e in lst:
        cnt = len(dict[e])
        if curr_cnt < cnt:
            curr_cnt = cnt
            curr_e = e
    return curr_e



def discrete_Morse_theory(ds: List[Set['Simplex']], rdict_p: dict, rdict_m: dict) -> Set['Simplex']:
    critical, removed = set(), set()
    que = set()
    k = set().union(*ds)
    while removed | critical != k:
        # pick currently the lowest dimension simplex
        for i in range(len(ds)):
            ds[i] -= removed | critical
        for di in ds:
            if len(di) > 0:
                # tau = random.choice(list(di))
                tau = simplex_argmax(list(di), rdict_p)
                break
        que = {tau}
        critical.add(tau)
        while que:
            alpha = que.pop()
            for beta in rdict_p[alpha]:
                rdict_m[beta] = rdict_m[beta] - removed - critical
                if len(rdict_m[beta]) == 0:
                    critical.add(beta)
                elif len(rdict_m[beta]) == 1:
                    gamma = rdict_m[beta].pop()
                    removed.add(gamma)
                    removed.add(beta)
                    rdict_p[gamma] = rdict_p[gamma] - removed - critical
                    rdict_p[beta] = rdict_p[beta] - removed - critical
                    que = que | rdict_p[gamma] | rdict_p[beta]

    return critical


# print(discrete_Morse_theory(ds, rdict_p_, rdict_m_))


def f(k):
    # generate graph with n simplex
    ds = random_generator(k)

    original_length.append(len(ds[0]) + len(ds[1]) +len(ds[2]))
    rdict_p_ = collections.defaultdict(set)
    rdict_m_ = collections.defaultdict(set)
    for i in range(len(ds)):
        for e in ds[i]:
            # high-level dimension
            if i < len(ds) - 1:
                rdict_p_[e] = {eh for eh in ds[i + 1] if len(eh - e) == 1}
            # low-level dimension
            if i > 0:
                rdict_m_[e] = {el for el in ds[i - 1] if len(e - el) == 1}

    t0 = time.time()
    critical_length.append(len(discrete_Morse_theory(ds, rdict_p_, rdict_m_)))
    t1 = time.time()

    return (t1 - t0)*10**3

Ns = []
ts = []

for k in range(3, 500):

    t = f(k)
    n = original_length[k-3] #sum([math.comb(k,j) for j in range(3)])
    print(k, n, critical_length[k-3], t)
    Ns.append(n)
    ts.append(t)

# plt.plot(Ns, ts)
plt.scatter(Ns, ts)
plt.title('Time Complexity')
plt.xlabel('Number of Original Simplices')
plt.ylabel('Time')
plt.show()

plt.scatter(original_length, critical_length)
plt.axline((0, 0), slope=1, color = 'green')
plt.title('Number of Original Simplices vs. Number of Critical Simplices')
plt.xlabel('Number of Original Simplices')
plt.ylabel('Number of Critical Simplices')
plt.show()

print("end")
