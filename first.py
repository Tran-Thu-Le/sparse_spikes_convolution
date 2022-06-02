import streamlit as st
from setup import process_input, set_up, plot

st.write("""
A vizualization of
# Sparse Spikes Convolution
""")


def get_user_input():
    positions = st.sidebar.text_input('positions of spikes', "[[0.1, 0.1], [0.5, 0.7], [0.9, 0.4]]")
    amplitudes = st.sidebar.text_input("amplitudes of spikes", "[1., 1., 0.6]")
    half_width = st.sidebar.slider('half_width', 0., 0.5, 0.1)
    contour_color = st.sidebar.selectbox('contour_color',('viridis','Blues', 'Reds'))
    spike_marker = st.sidebar.selectbox('spike_marker',('*','+', 's', 'x'))
    color_bar = st.sidebar.selectbox('color_bar',('off', 'on'))
    raw_data = {
        'positions': positions,
        'amplitudes': amplitudes,
        'half_width': half_width,
        'contour_color': contour_color,
        'spike_marker': spike_marker,
        'color_bar': color_bar,
    }
    return raw_data

if __name__=="__main__":
    raw_data = get_user_input()
    # raw_data = get_raw_input()# default raw data
    data = process_input(raw_data)
    setup = set_up(data)
    fig = plot(raw_data, data, setup)
    st.write(fig)

