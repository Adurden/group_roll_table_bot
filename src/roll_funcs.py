import numpy as np


def roll(num, face, mod=0):
    return np.random.randint(1+mod, face+1+mod, num)


def pass_distribution(num, face, dc, mod=0, tests=10000000):
    rolls = roll((tests, num), face, mod)
    num_passed = np.sum(rolls > dc, axis=1)
    num_passed, cnts = np.unique(num_passed, return_counts=True)
    return(cnts/tests)


def roll_table(num, face, dc, mod=0, tests=10000000):
    num, face, dc, mod = int(num), int(face), int(dc), int(mod)
    num_passed = pass_distribution(num, face, dc, mod, tests)
    hit_counts = np.where(num_passed > 0.05)[0]
    num_passed = num_passed[hit_counts]
    dist = np.round(num_passed/min(num_passed))
    num_splits = np.sum(dist)
    num_per_split = 20/num_splits
    num_per_cnt = np.round(dist*num_per_split)
    if np.sum(num_per_cnt) < 20:
        num_per_cnt[round(len(num_per_cnt)/2)] += 20 - np.sum(num_per_cnt)
    if np.sum(num_per_cnt) > 20:
        num_per_cnt[round(len(num_per_cnt)/2)] -= np.sum(num_per_cnt) - 20
    cur_key = 1
    roll_table = dict()
    for num_hit, rolls in zip(hit_counts, num_per_cnt):
        for i in range(cur_key, cur_key+int(rolls)):
            roll_table[i] = num_hit
        cur_key += int(rolls)
    return(roll_table)
