from math import comb

def epic_chance(total_size: int, n_desired: int, draw_size: int) -> float:
    """Calculate the probability of *actually* getting the player(s) you want 
       from an eFootball pack draw! Yeah, it'll be less than you think...

    :param int total_size: Number of remaining possible players left in the pack. 
        e.g. If it's a 250-player pack, and you already used the free chance, then enter "249".
    :param int n_desired: Number of players you actually care about still left in the pack. 
        e.g. If there are 7 epics and you don't really need 3 of them, then enter "4".
    :param int draw_size: The number of chances you're burning in one go. 
        e.g. If you're dropping 900 coins to get the discounted 10 chances, then enter "10".
    :raises ValueError: N/A
    :return float: Probability of getting what you want!
    """
    assert total_size >= n_desired and total_size >= draw_size
    n_undesired = total_size - n_desired

    # Let's fill a dictionary with the calculations. 
    # Let X be the random variable representing number of desired cards (e.g. epics) we actually draw. 
    # e.g. X=0 is the situation where we get no epics in our draw (very likely), 
    #      X=2 is the situation where we get 2 in our draw (very rare, and it triggers that special animation!).
    Prob_X_eq = {}
    for desired_drawn in range(0, n_desired+1):
        # i.e. Prob_X_eq_0 = comb(n_undesired, draw_size) / comb(total_size, draw_size)
        #      Prob_X_eq_1 = comb(n_desired, 1) * comb(n_undesired, draw_size-1) / comb(total_size, draw_size)
        #      ... etc.
        Prob_X_eq[desired_drawn] = (
            comb(n_desired, desired_drawn) * comb(n_undesired, draw_size-desired_drawn) 
            / comb(total_size, draw_size)
        )
    
    # Let's print the information so we completely understand it.
    Prob_X_geq_1 = 1 - Prob_X_eq[0]
    print(f"{Prob_X_geq_1*100:.1f}% chance that you'll get what you want (i.e. avoid the 0)! Worth it?\n")
    print("Here's the rest of the picture - chances of getting each number of "
          "desired players (e.g. epics) during this draw:\n")
    for n, chance in Prob_X_eq.items():
        print(f"{n}: {chance*100:.1f}%")
    return Prob_X_eq
