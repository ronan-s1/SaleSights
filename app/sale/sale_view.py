# sale_views.py
import streamlit as st
from sale.sale_controller import process_decoded_barcode
from streamlit_qrcode_scanner import qrcode_scanner


def scan_product(session_state):
    with st.expander("Scan Product"):
        # Create a state variable for the camera
        if "cam_on" not in session_state:
            session_state.cam_on = False

        # Add a button to toggle the camera on and off
        if st.button("Toggle Camera"):
            session_state.cam_on = not session_state.cam_on

        # If the camera is on, capture and display video frames
        if session_state.cam_on:
            barcode = qrcode_scanner(key="scanner")
            if barcode:
                scanned_product = process_decoded_barcode(barcode)
                return scanned_product


def sale_main():
    if "cam_on" not in st.session_state:
        st.session_state.cam_on = False

    scanned_product = scan_product(st.session_state)

    if scanned_product:
        st.write(scanned_product)
