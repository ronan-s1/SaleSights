import streamlit as st
from langchain.agents import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_models import ChatOpenAI
import pandas as pd
from biz.biz_data import (
    fetch_openai_api_key,
    fetch_model,
    fetch_expenses,
    fetch_expense_categories,
    fetch_products,
    fetch_product_categories,
    fetch_sale_transactions,
)


def get_greeting():
    """
    Returns a greeting message.

    Returns:
        response (str): Greeting message.
    """
    response = (
        "Hey there! I'm Biz, your AI data analysis assistant. How can I help you today?"
    )
    return response


def get_expenses_df():
    """
    Fetches the expenses and converts the data into a dataframe.

    Returns:
        df (pd.Dataframe): Dataframe containing the expenses.
    """

    expenses_data = fetch_expenses()
    df = pd.DataFrame(expenses_data)
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

    if len(selected_collections) <= 0:
        err = "Please select a collection to proceed."
        return None, err

    if len(selected_collections) == 1:
        return selected_collections[0], None

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

    llm = ChatOpenAI(
        temperature=0,
        model=get_model(),
        openai_api_key=get_openai_api_key(),
        streaming=True,
    )

    return llm


def instantiate_pandas_dataframe_agent(llm, selected_collections_df):
    """
    Instantiates the pandas dataframe agent.

    Args:
        llm (ChatOpenAI): OpenAI LLM model instance.
        selected_collections_df (list/pd.Dataframe): List of selected collections in dataframes or a single dataframe.

    Returns:
        pandas_df_agent (AgentType): An AgentExecutor with the specified agent_type agent and access to a PythonAstREPLTool with the DataFrame(s) and any user-provided extra_tools
    """

    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        selected_collections_df,
        verbose=True,
        max_iterations=8,
        max_execution_time=100,
        handle_parsing_errors=True,
    )

    return pandas_df_agent


def process_query(selected_collections_df):
    """
    Processes the user's query. If the query is valid, the agent's response is returned. If the query is invalid, a warning message is returned.

    Args:
        selected_collections_df (list/pd.Dataframe): List of selected collections in dataframes or a single dataframe.
    """
    llm = instantiate_openai_model()
    pandas_df_agent = instantiate_pandas_dataframe_agent(llm, selected_collections_df)

    # displays the agent's LLM and tool-usage thoughts
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)

    valid = True
    try:
        response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
    except:
        response = "Please ask a question related to the selected data."
        valid = False

    return response, valid
