import streamlit as st
from utils import epic_chance, generate_message
from contextlib import redirect_stdout
import io
import pandas as pd


# GUI heading
st.image('assets/efootball-banner-cropped.jpeg')
# SEO stuff; google "site:packprob.streamlit.app" to check this indexed meta info
st.set_page_config(page_title="packprob")   # SEO
st.title("packprob")
# NOTE: Search engines seem to use st.header() (<h2>) over st.title() (<h1>), prob because <h1> is often just one word...
st.header("eFootball Pack Probability Calculator")  # SEO
st.text("Calculate the probability of actually getting the player(s) you want from an eFootball pack draw!\n"
        "Yeah, it'll be less than you think...")    # SEO


# TODO: Sidebar with README from GitHub


# GUI base layout horizontal - left for inputs, right for outputs
# # Method 1: Horizontal base container
# base_cont = st.container(horizontal=True)
# left_cont = base_cont.container(border=True)
# right_cont = base_cont.container(border=True)
# Method 2: Columns; maybe more mobile-friendly?
# TODO: Try this, because horizontal container isn't working on mobile lol
left_cont, right_cont = st.columns(2, border=True)


with left_cont:
    # Fields for inputs from human user
    total_size = \
        st.number_input("Total pack size (remaining) 🟥:", 
                        value=250, min_value=1, step=10,
                        key='total_size',
                        help="e.g. If it's a 250-player pack, and you already used the free chance, then enter \"249\".")
    n_desired = \
        st.number_input("# of cards you want 🟦:", 
                        value=7, min_value=1, max_value=total_size,
                        key='n_desired',
                        help="e.g. If there are 7 epics and you don't really need 3 of them, then enter \"4\".")
    draw_size = \
        st.number_input("# of cards you'll draw 🟪:", 
                        value=10, min_value=1, max_value=total_size,
                        key='draw_size',
                        help="e.g. If you're dropping 900 coins to get the discounted 10 chances, then enter \"10\".")

    # Input validation
    # Well actually, st.number_input() ensures inputs always legal!
    # Otherwise, I would add a conditional:
    # st.error('Invalid number configuration...', icon="🚨")
    # st.warning('Invalid number configuration...', icon="🚨")
    # st.info('Invalid number configuration...', icon="🚨")

    # The execution trigger
    if st.button("Calculate!"):
        # st.info("Running the numbers...")   # Use either info or spinner
        with st.spinner("Running the numbers..."):
            try:
                # Plug inputs into the backend

                # # Method 1: redirect_stdout() to pipe print statements
                # # Problem: Can't cache epic_chance() outputs, because we'd need it to print every time!
                # f = io.StringIO()   # Capture all the print statements
                # with redirect_stdout(f):
                #     pulls_chance_dict = epic_chance(total_size, n_desired, draw_size, verbose=True)
                # message_md = f.getvalue()     # Collected print strings (assume already Markdown!)

                # Method 2: Take only the output dict of epic_chance(), then construct Markdown here
                pulls_chance_dict = epic_chance(total_size, n_desired, draw_size, verbose=False)
                message_md = generate_message(total_size, n_desired, draw_size, pulls_chance_dict, print_dict=False)

                st.session_state['output_markdown'] = message_md
                st.session_state['output_dict'] = pulls_chance_dict
            except Exception as e:
                st.exception(e)
    
    # Example screenshot of an eFootball campaign with colored squares highlighting what to input
    st.image('assets/pack-info-squares.png')
    st.image('assets/pack-desired-squares.png')


with right_cont:
    if 'output_dict' not in st.session_state:  # Check existence of result
        st.info("Waiting for your numbers...")
    else:
        # Print the final results for the human user
        # TODO: Make a chat message style print log, so we can see history!
        #       Requires using st.session_state to keep full list of printouts...
        # with st.container(border=True):
        with st.chat_message("assistant"):
            # The explanation
            # st.text(repr(st.session_state.output_markdown))   # For debugging Markdown newlines!
            st.success(st.session_state.output_markdown)

            # The table of probabilities
            out_ser = pd.Series(st.session_state.output_dict)
            out_ser.index.name = 'Pulls'
            out_ser.name = 'Chance'
            st.dataframe(
                out_ser,
                column_config={
                    'Chance': st.column_config.NumberColumn(
                        format='percent'
                    )
                }
            )
