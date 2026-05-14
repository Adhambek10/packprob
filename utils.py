from math import comb, isclose


def epic_chance(total_size: int, n_desired: int, draw_size: int) -> dict[int, float]:
    """Calculate the probability of *actually* getting the player(s) you want 
       from an eFootball pack draw! Yeah, it'll be less than you think...

       Example 1:
       Scenario: "It's a 150-player pack with 1 BigTime and 2 ShowTimes. I really want the BigTime, 
                  and I'm willing to roll 5 draws of 10 players each (spending 5*900=4500 coins)."
       Usage: epic_chance(150, 1, 5*10)
       Output: {0: 0.6666666666666666,
                1: 0.3333333333333333}
       "33.3% chance that you'll get something you want (i.e. avoid X=0)! Worth it?
        Here's the rest of the picture - chances of getting each number of desired players (e.g. epics) during this draw:
        0: 66.7%
        1: 33.3%"

       Example 2:
       Scenario: "It's a 250-player pack with 7 epics. I just started playing so would be happy with 
                  any of the 7. I just saved up 900 coins so can only roll once for 10 players! Konami 
                  did already give us 1 free roll, but I didn't get anything with that (obviously)."
       Usage: epic_chance(250-1, 7, 1*10)
       Output: {0: 0.7478759630652251,
                1: 0.22468376572775,
                2: 0.025925049891663464,
                3: 0.0014709248165482817,
                4: 4.362912591456768e-05,
                5: 6.627208999681165e-07,
                6: 4.640902660841153e-09,
                7: 1.109600158001471e-11}
       "25.2% chance that you'll get something you want (i.e. avoid X=0)! Worth it?
        Here's the rest of the picture - chances of getting each number of desired players (e.g. epics) during this draw:
        0: 74.8%
        1: 22.5%
        2: 2.6%
        3: 0.1%
        4: 0.0%
        5: 0.0%
        6: 0.0%
        7: 0.0%"

        Example 3:
        Scenario: "Woah, I just pulled BigTime Hazard AND epic Sneijder in my first 10-draw! I must be the 
                   luckiest person on the planet - I wonder what were the chances of pulling 2 epics including 
                   Hazard? It was a 250-pack (with a free roll) that had 7 epics including the BigTime."
        Analysis: This actually happened to me lol. We start by calculating the chance of pulling any 2 epics:
            Usage: epic_chance(250-1, 7, 10)
            Output: {0: 0.7478759630652251,
                     1: 0.22468376572775,
                     2: 0.025925049891663464,
                     3: 0.0014709248165482817,
                     4: 4.362912591456768e-05,
                     5: 6.627208999681165e-07,
                     6: 4.640902660841153e-09,
                     7: 1.109600158001471e-11}
                  So that's a 2.59% (~1 in 40) chance to start. But we were luckier than that - how many of these 
                  epic 2-combos include Hazard specifically? There are 7choose2=21 total combos, 6 of which include 
                  Hazard (just fix Hazard and then cycle through the other 6). That's a 2/7 chance on top of the 
                  2.59% - multiplying for concurrency we get 0.74%, or 1 in 135!
        Answer: So I am very lucky, but not the luckiest in the world! On average, 1 in every 135 players who 
                drew 10 experienced the same unforgettable Big Time double walkout animation. And as we know, 
                there are more than one million "serious" players competing in Divisions on mobile - if 1 million 
                went for the pack, then we'd estimate 1e6/135=7407 people had the same luck!

    :param int total_size: Number of remaining possible players left in the pack. 
        e.g. If it's a 250-player pack, and you already used the free chance, then enter "249".
    :param int n_desired: Number of players you actually care about still left in the pack. 
        e.g. If there are 7 epics and you don't really need 3 of them, then enter "4".
    :param int draw_size: The number of chances you're willing to spend. 
        e.g. If you're dropping 900 coins to get the discounted 10 chances, then enter "10".
    :raises ValueError: Never
    :return dict[int, float]: Mapping of "# of desired cards drawn" to "probability (out of 1)". 
                              Note then that 1-Prob_X_eq[0] would give you the probability of 
                              getting *something* you want (i.e. getting one or more desired cards)!
    """
    assert total_size > 0 and n_desired > 0 and draw_size > 0
    assert total_size >= n_desired and total_size >= draw_size
    n_undesired = total_size - n_desired

    # Let's fill a dictionary with the calculations. 
    # Let X be the random variable representing number of desired cards (e.g. epics) we actually draw. 
    # e.g. X=0 is the situation where we get no epics in our draw (very likely), 
    #      X=2 is the situation where we get 2 in our draw (very rare, and it triggers that special walkout animation!).
    Prob_X_eq = {}
    for desired_drawn in range(0, min(n_desired, draw_size)+1):     # min() avoids "evaluating X=2, but draw size was only 1"
        # i.e. Prob_X_eq_0 = comb(n_undesired, draw_size) / comb(total_size, draw_size)
        #      Prob_X_eq_1 = comb(n_desired, 1) * comb(n_undesired, draw_size-1) / comb(total_size, draw_size)
        #      ... etc.
        undesired_drawn = draw_size - desired_drawn
        assert undesired_drawn >= 0
        Prob_X_eq[desired_drawn] = (
            comb(n_desired, desired_drawn) * comb(n_undesired, undesired_drawn) 
            / comb(total_size, draw_size)
        )
    
    # Let's print the information so we completely understand it.
    Prob_X_geq_1 = 1 - Prob_X_eq[0]
    print(f"\n{Prob_X_geq_1*100:.1f}% chance that you'll get something you want (i.e. avoid X=0)! Worth it?\n")
    print("Here's the rest of the picture - chances of getting each number of "
          "desired players (e.g. epics) during this draw:\n")
    for n, chance in Prob_X_eq.items():
        print(f"{n}: {chance*100:.1f}%")
    assert isclose(sum(Prob_X_eq.values()), 1)
    return Prob_X_eq


import re
def text_to_markdown(my_text: str) -> str:
    """Convert the "\n"s in my print messages to Markdown's "  \n"s, but preserve my "\n\n"s

    :param str my_text: A print message.
    :return str: The print message but with newlines replaced for Markdown aesthetics.
    """
    # (?<!\n) means "not preceded by \n"
    # (?!\n)  means "not followed by \n"
    my_text_markdown = re.sub(r'(?<!\n)\n(?!\n)', '  \n', my_text)
    return my_text_markdown
