import streamlit as st
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_models import ChatOpenAI
from biz.biz_data import (
    fetch_openai_api_key,
    fetch_model,
    fetch_expenses,
    fetch_expense_categories,
    fetch_products,
    fetch_product_categories,
    fetch_sale_transactions,
)
from biz.utils.prompt_templates import (
    SINGLE_DF_PREFIX,
    SINGLE_DF_SUFFIX,
    MULTI_DF_PREFIX,
    MULTI_DF_SUFFIX,
)


def get_greeting():
    """
    Returns a greeting message.

    Returns:
        response (str): Greeting message.
    """
    response = "Hey there! I'm Biz, your AI data analysis assistant. [Need help?](https://salesights.xyz)"
    return response


def get_expenses_df():
    """
    Fetches the expenses and converts the data into a dataframe.

    Returns:
        df (pd.Dataframe): Dataframe containing the expenses.
    """

    expenses_data = fetch_expenses()
    df = pd.DataFrame(expenses_data)
    df.rename(columns={"_id": "expense_id"}, inplace=True)
    return df


def get_expenses_categories_df():
    """
    Fetches the expenses categories and converts the data into a dataframe.

    Returns:
        df (pd.Dataframe): Dataframe containing the expenses categories.
    """
    expenses_categories_data = fetch_expense_categories()
    df = pd.DataFrame(expenses_categories_data)
    return df


def get_products_df():
    """
    Fetches the products and converts the data into a dataframe.

    Returns:
        df (pd.Dataframe): Dataframe containing the products.
    """
    products_data = fetch_products()
    df = pd.DataFrame(products_data)
    return df


def get_product_categories_df():
    """
    Fetches the product categories and converts the data into a dataframe.

    Returns:
        df (pd.Dataframe): Dataframe containing the product categories.
    """
    product_categories_data = fetch_product_categories()
    df = pd.DataFrame(product_categories_data)
    return df


def flatten_transactions(transactions):
    """
    Flattens the transactions data into a list of dictionaries. Each product in a transaction is a separate dictionary.

    Args:
        transactions (list): List of transactions.

    Returns:
        flattened_transactions (list): List of dictionaries containing the flattened transactions.
    """
    if not transactions:
        return None

    flattened_transactions = []
    for transaction in transactions:
        transaction_id = transaction["_id"]
        date = transaction["date"]
        time = transaction["time"]
        total = transaction["total"]

        # flatten each product in the products list in the transaction
        for product in transaction["products"]:
            flattened_transaction = {
                "transaction_id": transaction_id,
                "date": date,
                "time": time,
                "total": total,
                "product_name": product["product_name"],
                "category": product["category"],
                "barcode_data": product["barcode_data"],
                "price": product["price"],
                "quantity": product["quantity"],
            }
            flattened_transactions.append(flattened_transaction)

    return flattened_transactions


def get_sale_transactions_df():
    """
    Fetches the sales transactions and flattens the data into a dataframe.

    Returns:
        df (pd.Dataframe): Dataframe containing the flattened sales transactions.
    """
    transactions = fetch_sale_transactions()
    flattened_transactions = flatten_transactions(transactions)

    if flattened_transactions is None:
        return pd.DataFrame()

    df = pd.DataFrame(flattened_transactions)
    return df


def selected_collections_processing(selected_collections):
    """
    Processes the selected collections. If no collection is selected, a warning message is returned. If only one collection is selected, the collection is returned. If multiple collections are selected, the list of collections is returned.

    Args:
        selected_collections (list): List of selected collections.

    Returns:
        response (str): Warning message or selected collection(s).
        valid (bool): Whether the selected collections are valid.
    """
    # if no collection is selected
    if len(selected_collections) <= 0:
        err = "Please select valid data to proceed."
        return None, err

    # if only one collection is selected
    if len(selected_collections) == 1:
        return selected_collections[0], None

    # if multiple collections are selected
    return selected_collections, None


def get_selected_collections(
    expenses_collection,
    expenses_categories_collection,
    products_collection,
    product_categories_collection,
    sales_transactions_collection,
):
    """
    Fetches the selected collections. If a collection is selected, the data is fetched and added to the selected_collections list.

    Args:
        expenses_collection (bool): Whether the expenses collection is selected.
        expenses_categories_collection (bool): Whether the expenses categories collection is selected.
        products_collection (bool): Whether the products collection is selected.
        product_categories_collection (bool): Whether the product categories collection is selected.
        sales_transactions_collection (bool): Whether the sales transactions collection is selected.

    Returns:
        selected_collections (list): List of selected collections. The collections are convereted to dataframes.
    """
    # list to store the selected collections
    selected_collections = []

    if expenses_collection:
        expenses_df = get_expenses_df()
        selected_collections.append(expenses_df)

    if expenses_categories_collection:
        expenses_categories_df = get_expenses_categories_df()
        selected_collections.append(expenses_categories_df)

    if products_collection:
        products_df = get_products_df()
        selected_collections.append(products_df)

    if product_categories_collection:
        products_categories_df = get_product_categories_df()
        selected_collections.append(products_categories_df)

    if sales_transactions_collection:
        sales_transactions_df = get_sale_transactions_df()
        selected_collections.append(sales_transactions_df)

    selected_collections, err = selected_collections_processing(selected_collections)

    return selected_collections, err


def get_model():
    """
    Fetches the GPT model from settings.

    Returns:
        model (str): Open AI model.
    """
    return fetch_model()


def get_openai_api_key():
    """
    Fetches the openAI API key from settings.

    Returns:
        openai_api_key (str): Open AI API key.
    """
    return fetch_openai_api_key()


def instantiate_openai_model():
    """
    Instantiates the OpenAI model.

    Returns:
        llm (ChatOpenAI): OpenAI LLM model instance with custom config.
    """
    openai_api_key = get_openai_api_key()
    model = get_model()

    if (openai_api_key is None) or (model is None):
        return None

    llm = ChatOpenAI(
        temperature=0,
        model=model,
        openai_api_key=openai_api_key,
        streaming=True,
    )

    return llm


def get_prefix_suffix(selected_collections_df):
    """
    Returns the prefix and suffix based on the number of selected collections.

    Args:
        selected_collections_df (list/pd.Dataframe): List of selected collections in dataframes or a single dataframe.

    Returns:
        prefix (str): Prefix message.
        suffix (str): Suffix message.
    """
    if isinstance(selected_collections_df, pd.DataFrame):
        return SINGLE_DF_PREFIX, SINGLE_DF_SUFFIX

    elif isinstance(selected_collections_df, list) and len(selected_collections_df) > 1:
        return MULTI_DF_PREFIX, MULTI_DF_SUFFIX

    return SINGLE_DF_PREFIX, SINGLE_DF_SUFFIX


def instantiate_pandas_dataframe_agent(llm, selected_collections_df):
    """
    Instantiates the pandas dataframe agent.

    Args:
        llm (ChatOpenAI): OpenAI LLM model instance.
        selected_collections_df (list/pd.Dataframe): List of selected collections in dataframes or a single dataframe.

    Returns:
        pandas_df_agent (AgentType): An AgentExecutor with the specified agent_type agent and access to a PythonAstREPLTool with the DataFrame(s) and any user-provided extra_tools
    """
    prefix, suffix = get_prefix_suffix(selected_collections_df)

    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        selected_collections_df,
        verbose=True,
        max_iterations=8,
        max_execution_time=100,
        handle_parsing_errors=True,
        prefix=prefix,
        suffix=suffix,
        include_df_in_prompt=None,
        input_variables=["df_head", "dfs_head", "num_dfs", "input", "agent_scratchpad"],
    )

    return pandas_df_agent


def process_query(selected_collections_df):
    """
    Processes the user's query. If the query is valid, the agent's response is returned. If the query is invalid, a warning message is returned.

    Args:
        selected_collections_df (list/pd.Dataframe): List of selected collections in dataframes or a single dataframe.

    Returns:
        response (str): Agent's response or warning message.
        valid (bool): If an error occurs, valid is False. Otherwise, valid is True.
    """
    # if an empty data is selected
    if (
        isinstance(selected_collections_df, pd.DataFrame)
        and selected_collections_df.empty
    ):
        return "Please select valid data to proceed.", False

    # Remove any empty collections from the list
    elif isinstance(selected_collections_df, list):
        selected_collections_df = [
            collection for collection in selected_collections_df if not collection.empty
        ]

        # if multiple collections are selected and all are empty
        if len(selected_collections_df) == 0:
            return "Please select valid data to proceed.", False

        # if only one collection is valid after removing empty collections
        if len(selected_collections_df) == 1:
            selected_collections_df = selected_collections_df[0]

    llm = instantiate_openai_model()

    if llm is None:
        return (
            "Please set your OpenAI API key and model in the settings to proceed.",
            False,
        )

    pandas_df_agent = instantiate_pandas_dataframe_agent(llm, selected_collections_df)

    # displays the agent's LLM and tool-usage thoughts
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
    valid = True
    try:
        response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
    except:
        response = "Make sure to ask a question related to the selected data. If you're stuck look at the [docs](https://salesights.xyz/)."
        valid = False

    return response, valid
