import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from matplotlib import colors
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


def st_image_cycler(image_list: list[str]) -> DeltaGenerator:
    """Very simplistic image carousel. 
       Problems:
         - Can't make multiple since the session_state key is fixed. 
         - The image refresh/reload is choppy. 
         - The "next" button gets wrapped around to the bottom if this cycler container is nested.

    :param list[str] image_list: E.g. ['assets/pack-info-squares.png', 'assets/pack-desired-squares.png']
    :return DeltaGenerator: The new container holding the image and the next button.
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


@st.cache_data
def highlight_relevant_chances(row) -> list[str]:
    """For use with Pandas: my_df.style.apply(highlight_relevant_chances, axis=1)

    :param row: pd.DataFrame row, where index can be accessed with .name
    :return list[str]: List of kwargs basically
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


def st_markdown_image_parser(text_md: str, container: DeltaGenerator = st) -> None:
    """Streamlit's st.write() can't parse images inside a Markdown README! So this runs 
       regex to identify images in Markdown text and render them separately using st.image().

    :param str text_md: The Markdown text imported as a string (i.e. using f.read())
    :param DeltaGenerator container: st.sidebar, st.container, etc.; defaults to None (just st)
    """
    if container is None:
        container = st  # So it'll be st.write(), etc.

    # Regex to capture image alt text (invisible), URL/path, and optional hover title
    pattern = r'!\[(?P<alt>[^\]]*)\]\((?P<url>[^\s\)]+)(?:\s+"(?P<title>[^"]*)")?\)'

    last_end = 0
    for match in re.finditer(pattern, text_md):
        # Grab standard text BEFORE this image match and render with st.write()
        text_before = text_md[last_end:match.start()]
        if text_before:
            container.write(text_before)
            
        # Grab the parsed image data and render with st.image()
        image_dict = match.groupdict()
        container.image(image_dict['url'], caption=image_dict['title'])
        
        last_end = match.end()  # Update position tracker

    # Catch any remaining text AFTER the final image
    remaining_text = text_md[last_end:]
    if remaining_text:
        container.write(remaining_text)
