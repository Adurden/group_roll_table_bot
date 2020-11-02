import numpy as np


def roll(num, face, mod=0):
    """
    a wrapper around numpy randint for generating a set dice rolls

    Parameters
    ----------
    num : int
        the number of dice inteded to be rolled
    face : int
        the number of faces on the dice being rolled
    mod : int
        a modifier to be added to the results of each roll

    Returns
    -------
    rolls : np.array
        a series of results from each roll
    """
    return np.random.randint(1+mod, face+1+mod, num)


def pass_distribution(num, face, dc, mod=0, tests=5000000, adv=-1):
    """
    rolls a large number of tests to simulate a distrubtion of numbers of
    passes from a number of attempts

    Parameters
    ----------
    num : int
        the number of attempts in a single test
    face : int
        the number of faces on the roll for the test
    dc : int
        the value needed to succeed
    mod : int, default = 0
        the value to be added to each attempt
    tests : int, default = 10,000,000
        the number of tests to simulate
    adv : bool
        if true give all dice

    Returns
    -------
    distrubtion : np.array
        an array giving the distrubtion of pass counts where the count is the
        index. i.e. [0.25, 0.5, 0.25] would be a 1/4 cahnce for 0 passes etc.
    """
    if adv < 0:
        print((tests, num, 2), face, mod)
        rolls = roll((tests, num, 2), face, mod)
        adv_passed = np.sum(rolls > dc, axis=2)
        adv_passed[adv_passed > 1] = 1
        num_passed = np.sum(adv_passed, axis=1)

    else:
        rolls = roll((tests, num), face, mod)
        num_passed = np.sum(rolls > dc, axis=1)
    num_passed, cnts = np.unique(num_passed, return_counts=True)
    return(cnts/tests)


def roll_table(num, face, dc, mod=0, tests=5000000, adv=-1):
    """
    build a roll table applying a pass distrubtion to a single d20 roll

    Parameters
    ----------
    num : int
        the number of attempts in a single test
    face : int
        the number of faces on the roll for the test
    dc : int
        the value needed to succeed
    mod : int, default = 0
        the value to be added to each attempt
    tests : int, default = 10,000,000
        the number of tests to simulate

    Returns
    -------
    roll_table : dict
        a dict giving the number of passes for a given result of a single d20
        roll to mimic the chances of a full roll's success counts where the
        keys are 1-20 and the vals are the number of passes
    """
    # cast input to int for discord command parse should move to the bot call
    num, face, dc, mod = int(num), int(face), int(dc), int(mod)

    # get the distribution of successes
    num_passed = pass_distribution(num, face, dc, mod, tests, adv)

    # filter for more than 1 in 20 chance
    hit_counts = np.where(num_passed > 0.05)[0]
    num_passed = num_passed[hit_counts]

    # assign a number of rolls to each distribution value
    dist = np.round(num_passed/min(num_passed))
    num_splits = np.sum(dist)
    num_per_split = 20/num_splits
    num_per_cnt = np.round(dist*num_per_split)

    # correct to 20 from rounding errrors
    if np.sum(num_per_cnt) < 20:
        num_per_cnt[round(len(num_per_cnt)/2)] += 20 - np.sum(num_per_cnt)
    if np.sum(num_per_cnt) > 20:
        num_per_cnt[round(len(num_per_cnt)/2)] -= np.sum(num_per_cnt) - 20

    # build roll table
    cur_key = 1
    roll_table = dict()
    for num_hit, rolls in zip(hit_counts, num_per_cnt):
        for i in range(cur_key, cur_key+int(rolls)):
            roll_table[i] = num_hit
        cur_key += int(rolls)
    return(roll_table)
