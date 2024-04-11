from settings.settings_data import insert_new_settings_to_db, fetch_settings


def update_settings(business_name, selected_model, api_key):
    """
    Request data access to update settings

    Args:
        business_name (str): The name of the business.
        selected_model (str): The selected theme for the chatbot.
        api_key (str): The OpenAI API key.

    Returns:
        str: Error message
        None: No errors
    """
    if any(not data for data in [business_name, selected_model, api_key]):
        return "Please fill in required fields"

    settings = {
        "business_name": business_name,
        "selected_model": selected_model,
        "openai_api_key": api_key,
    }

    insert_new_settings_to_db(settings)


def get_settings():
    """
    Request data access to fetch settings

    Returns:
        dict: The settings
    """
    settings = fetch_settings()
    models = ["gpt-4-turbo", "gpt-3.5-turbo-0125"]

    # if no settings exist, return default values
    if settings is None:
        return "", 0, "", models

    business_name = settings.get("business_name", "")
    api_key = settings.get("openai_api_key", "")

    selected_model = settings.get("selected_model", models[0])
    selected_model_index = (
        models.index(selected_model) if selected_model in models else 0
    )

    return business_name, selected_model_index, api_key, models
