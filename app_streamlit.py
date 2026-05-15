import streamlit as st
from utils import epic_chance, text_to_markdown
from contextlib import redirect_stdout
import io
import re

# GUI heading
# SEO stuff; google "site:packprob.streamlit.app" to check this indexed meta info
st.set_page_config(page_title="packprob")   # SEO
st.title("packprob")
# NOTE: Search engines seem to use st.header() (<h2>) over st.title() (<h1>), prob because <h1> is often just one word...
st.header("eFootball Pack Probability Calculator")  # SEO
st.text("Calculate the probability of actually getting the player(s) you want from an eFootball pack draw!\n"
        "Yeah, it'll be less than you think...")    # SEO

# GUI base layout horizontal - left for inputs, right for outputs
base_cont = st.container(horizontal=True)
left_cont = base_cont.container(border=True)
right_cont = base_cont.container(border=True)
# Alternate method for doing horizontal layout, maybe more mobile-friendly?
# left_cont, right_cont = st.columns(2, border=True)

with left_cont:
    # Fields for inputs from human user
    total_size = \
        st.number_input("Total pack size (remaining):", 
                        value=250, min_value=1, step=10,
                        key='total_size')   # TODO: Add hover tooltip description
    n_desired = \
        st.number_input("# of cards you like:", 
                        value=7, min_value=1, max_value=total_size,
                        key='n_desired')
    draw_size = \
        st.number_input("# of cards you'll draw:", 
                        value=10, min_value=1, max_value=total_size,
                        key='draw_size')

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
                f = io.StringIO()   # Capture all the print statements
                with redirect_stdout(f):
                    result = epic_chance(total_size, n_desired, draw_size)  # TODO: Make epic_chance() prints Markdown-friendly
                f_prints = f.getvalue()     # Collected print strings
                f_prints_markdown = text_to_markdown(f_prints)  # Convert the newlines to Markdown?
                st.session_state['output_markdown'] = f_prints_markdown  # TODO: Put output Markdown into session state
            except Exception as e:
                st.exception(e)
    
    # TODO: Add screenshot of an eFootball campaign with colored squares for reference

with right_cont:
    if 'output_markdown' not in st.session_state:    # Check existence of result
        st.info("Waiting for your numbers...")
    else:
        # Print of the final results for the human user
        # TODO: Make a chat message style print log, so we can see history!
        st.success(st.session_state.output_markdown)
