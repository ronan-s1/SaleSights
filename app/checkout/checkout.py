import streamlit as st
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar


def checkout_main():
    with st.expander("Scan Product"):
        # Create a state variable for the camera
        if "cam_on" not in st.session_state:
            st.session_state.cam_on = False

        # Add a button to toggle the camera on and off
        if st.button("Toggle Camera"):
            st.session_state.cam_on = not st.session_state.cam_on

        # If the camera is on, capture and display video frames
        if st.session_state.cam_on:
            cap = cv2.VideoCapture(0)
            frame_placeholder = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.write("The video capture has ended.")
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Scan the frame for barcodes
                decoded_objects = pyzbar.decode(frame)
                for obj in decoded_objects:
                    barcode_type = obj.type
                    barcode_data = obj.data.decode("utf-8")

                    # Only print the barcode if it's not already printed
                    if barcode_data not in st.session_state:
                        st.write(f"Barcode Type: {barcode_type}")
                        st.write(f"Barcode Data: {barcode_data}")
                        st.session_state[barcode_data] = True

                    # Draw a rectangle around the barcode
                    p1 = (obj.rect.left, obj.rect.top)
                    p2 = (
                        obj.rect.left + obj.rect.width,
                        obj.rect.top + obj.rect.height,
                    )
                    cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)

                frame_placeholder.image(frame, channels="RGB")

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()

# Run the checkout_main function
checkout_main()
