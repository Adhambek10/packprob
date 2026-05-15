import streamlit as st
import numpy as np
import pandas as pd

# Keep in mind that streamlit re-runs this whole file any time a button is touched!

# Static table using st.table()
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)

# # Interactive mode using st.dataframe()
# dataframe = np.random.randn(10, 20)
# st.dataframe(dataframe)

# pandas Styler object
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.dataframe(dataframe.style.highlight_max(axis=0))

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])
st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.map(map_data)

# st.session_state.burr  # AttributeError on very first run (but not if you already assigned it earlier in session)
x = st.slider('x', key='burr')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

# st.session_state.name     # AttributeError
st.text_input("Your name", key="name")
st.session_state.name

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c']
    )
    chart_data

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })
option = st.selectbox(
    'Which number do you like best?',
    df['first column']
)
'You selected: ', option

# Sidebar
# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)
add_selectbox
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
add_slider  # Shows a tuple

# Columns
left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
if left_column.button('Press me!'):
    left_column.write("*pressed*!")
# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

import time
# with st.echo():     # Show the code block after it finishes too!
#     'Starting a long computation...'
#     latest_iteration = st.empty()   # Placeholder widget that literally only takes up space on the page for now
#     bar = st.progress(0)    # Next widget under placeholder
#     for i in range(1, 100+1):
#         # Update the progress bar with each iteration.
#         latest_iteration.text(f'Iteration {i}')     # Placeholder now shows this text!
#         bar.progress(i)
#         time.sleep(0.1)
#     '...and now we\'re done!'

# Caching! Cached values work across many users across all sessions btw
@st.cache_data
def long_running_function(param1, param2):
    'Starting a long computation...'
    latest_iteration = st.empty()   # Placeholder widget that literally only takes up space on the page for now
    bar = st.progress(0)    # Next widget under placeholder
    for i in range(1, 100+1):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i}')     # Placeholder now shows this text!
        bar.progress(i)
        time.sleep(0.1)
    return '...and now we\'re done!'
st.write(long_running_function(1, 2))
'alright now again'
st.write(long_running_function(1, 2))

# Session state - only for the user's current tab session (since refresh)
if "counter" not in st.session_state:
    st.session_state.counter = 0
st.session_state.counter += 1
st.header(f"This page has run {st.session_state.counter} times.")
st.subheader(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")

# Keep same random DF within the session
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])
st.header("Choose a datapoint color")
color = st.color_picker("Color", "#FF0000")
st.divider()
st.scatter_chart(st.session_state.df, x="x", y="y", color=color)

# SEO - meta title and meta description
st.set_page_config(page_title="Traingenerator")
st.header("This might get grabbed by search engines as meta description")
st.text("this also might get grabbed by search engines as meta description")
# Google "site:<your-custom-subdomain>.streamlit.app" to check your indexed meta information

#########

# Layouts and containers (for out of order)

with st.container():
    st.write("Text inside the container")
    st.button("A button inside the container")

c = st.container()
c.write("Text inside the container")
c.button("A button inside the container fdsa")  # Huh, can't be the same text as the one above...

with st.container(border=True):
    st.write("This has a border around it.")

col1, col2, col3 = st.columns(3)
col1.metric("Revenue", "$12K", "8%")
col2.metric("Users", "1,204", "12%")
col3.metric("Latency", "42ms", "-3%")

left, right = st.columns([2, 1], border=True)
left.write("This column is twice as wide.")
right.write("This column is narrower.")

with st.expander("Show details"):
    st.write("Here are the details...")
    st.image("https://static.streamlit.io/examples/dice.jpg")

tab1, tab2, tab3 = st.tabs(["Chart", "Data", "Settings"])
with tab1:
    st.line_chart({"data": [1, 5, 2, 6, 2, 1]})
with tab2:
    st.dataframe({"col1": [1, 2, 3], "col2": [4, 5, 6]})
with tab3:
    st.checkbox("Show gridlines")

with st.popover("Filter settings"):
    st.checkbox("Include archived")
    st.slider("Min score", 0, 100, 50)

placeholder = st.empty()
for i in range(2):
    placeholder.write(f"Iteration {i}")
    time.sleep(0.5)
    placeholder.empty()
# Note the difference between st.container() and st.empty() is that empty() 
# only holds 1 element, i.e. it's designed for you to .write() to it to overwrite
# st.empty() is designed for updating display in place! The 1 element inside can 
# be a container, so you can update many things in place!

# Horizontal containers!
with st.container(horizontal=True):
    st.button("One")
    st.button("Two")
    st.button("Three")

with st.container(horizontal=True):
    st.text_input("Name")
    st.text_input("Email")
    st.date_input("Birthday")

with st.container(horizontal=True, horizontal_alignment="right"):
    st.button("Cancel")
    st.button("Submit")

# Spacing
col1, col2 = st.columns(2, gap="large", border=True)
col1.write("Wide gap between columns")
col2.write("See the space?")
# Manual spacing
st.write("Above")
st.space("large")
st.write("Below, after a large gap")

# Scrollable container!
with st.container(height=200):
    for i in range(20):
        st.write(f"Line {i}")

append_test_container = st.container(height=500)    # Doesn't scroll to bottom without st.chat_message()!
with append_test_container:
    for i in range(20):
        with st.chat_message(name='assistant'):
            st.write(f"Line {i}")
    for i in range(3):
        with st.chat_message(name='assistant'):
            st.write("append")

st.divider()

# Following code from Nicholas5
# https://discuss.streamlit.io/t/have-a-text-area-automatically-scroll-to-the-bottom/111090

_LONG_TEXT = """Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
"""

# Decrease superfluous padding on chat_message.
st.html("""
<style>
.stChatMessage {
    padding-top: 0;
    padding-bottom: 0;
}
</style>
""")

def generate_description():
    new_container = st.container(height=100)
    with new_container:
        for line in _LONG_TEXT.splitlines():
            chat_line = ""
            with st.chat_message("assistant"):
                chat_message = st.empty()
                for char in line:
                    chat_line += char
                    chat_message.markdown(chat_line)
                    time.sleep(0.025)
    return new_container

click = st.button('Stream Description')
rick_space = st.empty()
# rick_space = None
if click:
    rick_space.empty()  # Ahh due to how Streamlit redraws its UI, it will look like the container didn't really clear - it's just faded
    # time.sleep(5)
    # rick_space.empty()
    with rick_space:
        filled_container = generate_description()
    # rick_space.empty()
if st.button("clear"):
    rick_space.empty()

####
# Dynamic stuff

tab1, tab2 = st.tabs(["Chart", "Data"], on_change="rerun")  # Need this kwarg to activate .open checking

if tab1.open:
    with st.spinner("Loading Tab 1..."):
        time.sleep(2)
    with tab1:
        st.line_chart({"data": [1, 5, 2, 6]})

if tab2.open:
    with st.spinner("Loading Tab 2..."):
        time.sleep(2)
    with tab2:
        st.dataframe({"col1": [1, 2, 3]})

# Callbacks
def on_tab_change():
    st.toast(f"Tab changed to {st.session_state.tabs}!")

tab1, tab2 = st.tabs(["Input", "Output"], on_change=on_tab_change, key="tabs")

# Programmatic control
def toggle_expander():
    st.session_state.details = not st.session_state.details

exp = st.expander("Details", key="details", on_change="rerun")

with exp:
    st.write("Detailed content here")

st.button("Toggle expander", on_click=toggle_expander)

# Nesting containers
tab1, tab2 = st.tabs(["Overview", "Details"])

with tab1:
    col1, col2 = st.columns(2, border=True)
    col1.metric("Users", "1,204")
    col2.metric("Revenue", "$12K")

with tab2:
    with st.expander("Advanced settings"):
        thresh = st.slider("Threshold", 0.0, 1.0, 0.5)
thresh
