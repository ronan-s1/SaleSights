import streamlit as st
from settings.settings_controller import update_settings, get_settings


def settings_main():
    st.title("Settings ⚙️")

    business_name, selected_model_index, api_key, models = get_settings()

    updated_business_name = st.text_input("Business Name", value=business_name)
    updated_selected_model = st.selectbox(
        "Biz Chatbot Model", models, index=selected_model_index
    )
    updated_api_key = st.text_input("OpenAI API Key", type="password", value=api_key)

    if st.button("Save"):
        err = update_settings(
            updated_business_name, updated_selected_model, updated_api_key
        )
        if err:
            st.error(err)
        else:
            st.success("Settings updated")
