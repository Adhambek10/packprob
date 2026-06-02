import streamlit as st
from src import epic_chance, generate_message
from utils import st_markdown_image_parser, st_save_to_chatbot, st_display_chatbot_packprob


# # Manually adjust Streamlit "centered" page width - default 46rem
# st.html(
#     """
#     <style>
#         .stMainBlockContainer {
#             max-width:46rem;
#         }
#     </style>
#     """
# )


# GUI heading
st.image('assets/efootball-banner-cropped.jpeg')
# SEO stuff; google "site:packprob.streamlit.app" to check this indexed meta info
st.set_page_config(page_title="packprob")   # SEO
st.title("packprob")
# NOTE: Search engines seem to use st.header() (<h2>) over st.title() (<h1>), prob because <h1> is often just one word...
st.header("eFootball Pack Probability Calculator")  # SEO
st.text("Calculate the probability of actually getting the player(s) you want from an eFootball pack draw!\n"
        "Yeah, it'll be less than you think...")    # SEO


# Sidebar with README from GitHub
with open('README_sidebar.md', 'r', encoding='utf-8') as file:
    readme_md = file.read()
st_markdown_image_parser(readme_md, st.sidebar)     # Better version of st.sidebar.write(readme_md)


# GUI base layout horizontal - left for inputs, right for outputs
# # Method 1: Horizontal base container
# # Problem: Doesn't auto-switch to vertical layout for mobile!
# base_cont = st.container(horizontal=True)
# left_cont = base_cont.container(border=True)
# right_cont = base_cont.container(border=True)
# Method 2: Columns as base container - more mobile-friendly!
left_cont, right_cont = st.columns(2, border=True)


with left_cont:
    # Example screenshot of an eFootball campaign with colored squares highlighting what to input
    # Method 1: Simple, single image
    # NOTE: Can't URL link to other local images
    st.image('assets/pack-info-squares.png', caption='Colored boxes show where you can find the inputs.')
    # # Method 2: Make a container cycle images when you click next, like a slideshow
    # # Problem: Choppy and not very nice looking...
    # from utils import st_image_cycler
    # st_image_cycler(['assets/pack-info-squares.png', 'assets/pack-desired-squares.png'])
    # # Method 3: Use streamlit-carousel package for nice Bootstrap carousel
    # # Problem: Sizing is tricky, and there's no zoom on the images!
    # from streamlit_carousel import carousel
    # INPUT_TUTORIAL = [
    #     dict(
    #         # title="Slide 1",
    #         title=None,
    #         # text="Colored boxes show where you can find the inputs.",
    #         text=None,
    #         img='assets/pack-info-squares.png'
    #     ),
    #     dict(
    #         # title="Slide 2",
    #         title=None,
    #         # text="More detail on the blue box, i.e. counting the 7 epic cards in the pack.",
    #         text=None,
    #         img='assets/pack-desired-squares.png'
    #     ),
    # ]
    # carousel(items=INPUT_TUTORIAL, container_height=200, indicators=False, interval=None)

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
                        value=10, min_value=1, max_value=total_size, step=10,
                        key='draw_size',
                        help="e.g. If you're dropping 900 coins to get the discounted 10 chances, then enter \"10\".")

    # Input validation
    # Well actually, st.number_input() ensures inputs always legal!
    # Otherwise, I would add a conditional:
    # st.error('Invalid number configuration...', icon="🚨")
    # st.warning('Invalid number configuration...', icon="🚨")
    # st.info('Invalid number configuration...', icon="🚨")

    # The execution trigger
    # NOTE: Implemented continuous calculation checkbox using state checks here, instead of with callbacks on input fields!
    # Container to hold button, checkbox, and info
    calc_cont = st.container(horizontal=True, 
                             height=100,      # NOTE: Fixed height to prevent shifting content!
                             horizontal_alignment='center', vertical_alignment='center', 
                             border=False)   # For debugging
    # (Left) container to hold button (top) and checkbox (bottom)
    calc_checkbox_cont = calc_cont.container(width=104, horizontal_alignment='center', border=False)
    button_placeholder = calc_checkbox_cont.empty()     # Overly complex, but want 1) button above checkbox and 2) for button to react to checkbox!
    calc_checkbox = calc_checkbox_cont.checkbox('Continuous', key='calc_checkbox')   # Bottom
    calc_button = button_placeholder.button("Calculate!", disabled=st.session_state.calc_checkbox)   # Top
    # (Right) container to hold info
    info_placeholder = calc_cont.empty()
    if calc_button or calc_checkbox:
        # st.info("Running the numbers...")   # Use either info or spinner
        with st.spinner("Running the numbers..."):
            try:
                # Plug inputs into the backend

                # # Method 1: redirect_stdout() to pipe print statements
                # # Problem: Can't cache epic_chance() outputs, because we'd need it to print every time!
                # from contextlib import redirect_stdout
                # import io
                # f = io.StringIO()   # Capture all the print statements
                # with redirect_stdout(f):
                #     pulls_chance_dict = epic_chance(total_size, n_desired, draw_size, verbose=True)
                # message_md = f.getvalue()     # Collected print strings (assume already Markdown!)

                # Method 2: Take only the output dict of epic_chance(), then construct Markdown here
                pulls_chance_dict = epic_chance(total_size, n_desired, draw_size, verbose=False)
                message_md = generate_message(total_size, n_desired, draw_size, pulls_chance_dict, print_dict=False)

                # Save outputs into st.session_state's chat history (in style of Streamlit conversational app)
                content = {
                    'output_markdown': message_md,
                    'output_dict': pulls_chance_dict
                }

                # Store content depending on output panel

                # # Method 1: For simple refreshing output panel
                # st_save_to_chatbot(content, history=False)
                
                # Method 2: For scrollable chatbox output panel
                # Set history=True to enable chat history, beyond just the 1 most recent content.
                # Problem: Just kind of confusing and unnecessary, but was fun to build.
                st_save_to_chatbot(f"{total_size}-{n_desired}-{draw_size}", 'user', history=True)     # This is unnecessary I think
                st_save_to_chatbot(content, 'assistant', history=True)
            except Exception as e:
                st.exception(e)
        st.toast("Calculation complete.", icon='✅')
        info_placeholder.info("If on mobile, scroll down for results!", icon='📲', width=184)   # NOTE: Fixed width to prevent shifting content


with right_cont:
    if 'messages' not in st.session_state:  # Check existence of result
        st.info("Waiting for your numbers...")
    else:
        # Print the final results for the human user
        
        # # Method 1: Simple refreshing output panel
        # st_display_chatbot_packprob()

        # Method 2: Scrollable chatbox output panel
        # Make a chat message style print log - can see history of calculations!
        # Problem: Just kind of confusing and unnecessary, but was fun to build.
        with st.container(height=625, border=False):
            # NOTE that I've fixed the height to enable scrollbar, but I've also had to decrease the 
            # width of the chat messages to avoid a horizontal scrollbar that appears because Streamlit 
            # can't properly calculate the content size when nested containers are involved.
            st_display_chatbot_packprob(width=293)  # width=303 when no vertical scrollbar...
