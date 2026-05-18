from math import comb, isclose
import streamlit as st
from matplotlib import colors


@st.cache_data    # Beware, this stops the function from making print statements!
def epic_chance(total_size: int, n_desired: int, draw_size: int, verbose: bool = True) -> dict[int, float]:
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
    
    if verbose:  # Alternatively, user may just want the output dict so they can format it in Pandas, etc.
        # Let's print the information so we completely understand it.
        # NOTE: We're printing in Markdown format, where '\n\n' is a spaced newline, and '  \n' is a non-spaced newline.
        message_md = generate_message(total_size, n_desired, draw_size, Prob_X_eq, print_dict=True)
        print(message_md)

    assert isclose(sum(Prob_X_eq.values()), 1)
    return Prob_X_eq


@st.cache_data
def generate_message(total_size, n_desired, draw_size, pulls_chance_dict, print_dict=True):
    Prob_X_geq_1 = 1 - pulls_chance_dict[0]     # Prob_X_geq_1 = 1 - Prob_X_eq[0]
    # NOTE: We're writing in the Markdown format, where '\n\n' is a spaced newline, and '  \n' is a non-spaced newline.
    out_str = (
        "----  \n"
        f"{total_size}-{n_desired}-{draw_size}\n\n"
        f"**{Prob_X_geq_1*100:.1f}%** chance that you'll pull at least one! Worth it?\n\n"
    )
    if print_dict:
        extend_str = (
            "Here's the rest of the picture - **chance** of getting each number of "
            "**desired** cards (e.g. epic players) while drawing:\n\n"
        )
        for n, chance in pulls_chance_dict.items():
            extend_str += f"{n} pulls: **{chance*100:.1f}%**  \n"
        extend_str += '\n'  # End it with a nice spaced newline
        out_str += extend_str
    return out_str


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


def st_image_cycler(image_list: list[str]) -> st.delta_generator.DeltaGenerator:
    """Very simplistic image carousel. 
       Problems:
         - Can't make multiple since the session_state key is fixed. 
         - The image refresh/reload is choppy. 
         - The "next" button gets wrapped around to the bottom if this cycler container is nested.

    :param list[str] image_list: e.g. ['assets/pack-info-squares.png', 'assets/pack-desired-squares.png']
    :return st.delta_generator.DeltaGenerator: The new container holding the image and the next button.
    """
    assert len(image_list) > 0

    if 'image_cycler_curr_idx' not in st.session_state:
        # Set up internal session state needed
        st.session_state['image_cycler_len'] = len(image_list)
        st.session_state['image_cycler_list'] = image_list
        st.session_state['image_cycler_curr_idx'] = 0
    
    # Set up horizontal container with image and next button
    base_cont = st.container(horizontal=True, border=True,
                             horizontal_alignment='right',
                             vertical_alignment='center')   # Alignments mainly for the button

    # Left: Image
    image_placeholder = base_cont.empty()
    image_placeholder.image(st.session_state.image_cycler_list[st.session_state.image_cycler_curr_idx])
    
    # Right: Next button
    # NOTE: This doesn't work well when nested into another container; 
    #       the width of the external container forces the button underneath, rather than to the right.
    next_button = base_cont.button('⏭️')
    if next_button:
        st.session_state.image_cycler_curr_idx = (st.session_state.image_cycler_curr_idx + 1) % st.session_state.image_cycler_len
        image_placeholder.image(st.session_state.image_cycler_list[st.session_state.image_cycler_curr_idx])
    
    return base_cont    # Really don't need to return this...


def highlight_relevant_chances(row) -> list[str]:
    """For use with Pandas: my_df.style.apply(highlight_relevant_chances, axis=1)

    :param _type_ row: pd.DataFrame row, where index can be accessed with .name
    :return _type_: list of kwargs basically
    """
    # Apply a gradient green based on percent of success

    # Since we'll rarely see "high" pack luck, let's normalize and clip
    norm = colors.Normalize(vmin=0, vmax=0.5, clip=True)

    # Skip the Pulls=0 row - it will be high percent, but it's a bad thing
    if row.name == 0:   # row.name is index named "Pulls"
        # return [''] * len(row)    # For rows we don't want to highlight
        # return ['background-color: red'] * len(row)
        my_bad_cmap = colors.LinearSegmentedColormap.from_list(
            "red_transparent", 
            [(0.75, 0, 0, 0), (0.75, 0, 0, 1)]
        )
        rgba = my_bad_cmap(norm(row['Raw Chance']))
        hex_color = colors.to_hex(rgba, keep_alpha=True)    # Very important to keep the alpha for transparency!
        return [f'background-color: {hex_color}'] * len(row)

    # For other rows: calculate gradient color from matplotlib
    # if row.name > 0 and row.name <= 3:
        # return ['background-color: darkgreen'] * len(row)
    # cmap = plt.get_cmap('Greens')     # I want the low end to be transparent for dark mode, not white!
    my_good_cmap = colors.LinearSegmentedColormap.from_list(
        "green_transparent", 
        [(0, 0.75, 0, 0), (0, 0.75, 0, 1)]
    )
    rgba = my_good_cmap(norm(row['Raw Chance']))
    hex_color = colors.to_hex(rgba, keep_alpha=True)    # Very important to keep the alpha for transparency!
    return [f'background-color: {hex_color}'] * len(row)


def activate_invisible_containers():
    # Run this script to inject CSS defining invisible containers
    # Then use: 
    # st.markdown('<div class="invisible-container">', unsafe_allow_html=True)
    # MY CONTENT CONTAINER
    # st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        .invisible-container {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def begin_invisible_container():
    st.markdown('<div class="invisible-container">', unsafe_allow_html=True)

def end_invisible_container():
    st.markdown('</div>', unsafe_allow_html=True)
