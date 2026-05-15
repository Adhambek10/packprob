import streamlit as st

def st_image_cycler(image_list: list[str]) -> st.delta_generator.DeltaGenerator:
    assert len(image_list) > 0

    if 'image_cycler_curr_idx' not in st.session_state:
        # Set up internal session state needed
        st.session_state['image_cycler_len'] = len(image_list)
        st.session_state['image_cycler_list'] = image_list
        st.session_state['image_cycler_curr_idx'] = 0
    
    # Set up horizontal container with image and next button
    base_cont = st.container(horizontal=True, border=True)
    # Image
    # left_cont = base_cont.container(border=False)

    # image_placeholder = base_cont.empty()
    # image_placeholder.image(st.session_state.image_cycler_list[st.session_state.image_cycler_curr_idx])

    burr_button = base_cont.button('burr')
    # Next button
    # right_cont = base_cont.container(border=False)
    # TODO: Why isn't this horizontal?
    # with st.container(horizontal=True):
    #     st.image(st.session_state.image_cycler_list[st.session_state.image_cycler_curr_idx])
    #     st.button("⏭️")
    next_button = base_cont.button('⏭️')
    # if next_button:
    #     st.session_state.image_cycler_curr_idx = (st.session_state.image_cycler_curr_idx + 1) % st.session_state.image_cycler_len
    #     image_placeholder.image(st.session_state.image_cycler_list[st.session_state.image_cycler_curr_idx])
    return base_cont

st_image_cycler(['../assets/pack-info-squares.png', '../assets/pack-desired-squares.png'])
