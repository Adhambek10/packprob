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

# Layouts and containers

