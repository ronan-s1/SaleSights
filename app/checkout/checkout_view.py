# checkout_views.py
import streamlit as st
from checkout.checkout_controller import process_frame
import cv2

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
            cap = cv2.VideoCapture(0)
            frame_placeholder = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.write("The video capture has ended.")
                    break

                result = process_frame(frame, session_state)
                if result:
                    barcode_data = result["barcode_data"]
                    rectangle_coords = result["rectangle_coords"]

                    st.write(f"Barcode Data: {barcode_data}")

                    # Draw a rectangle around the barcode
                    cv2.rectangle(frame, rectangle_coords[:2], rectangle_coords[2:], (0, 255, 0), 2)

                frame_placeholder.image(frame, channels="BGR")

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()

def checkout_main():
    if "cam_on" not in st.session_state:
        st.session_state.cam_on = False
    
    scan_product(st.session_state)
