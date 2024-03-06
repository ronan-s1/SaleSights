import streamlit as st
from biz.biz_controller import (
    process_query,
    get_greeting,
    get_selected_collections,
)


def button_style():
    st.markdown(
        """
        <style>
            button {
                padding-top: 10.2px !important;
                padding-bottom: 10.2px !important;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )


def cache_selected_collections_df(
    expenses_collection,
    expenses_categories_collection,
    products_collection,
    product_categories_collection,
    sales_transactions_collection,
):

    selected_collections_df, err = get_selected_collections(
        expenses_collection,
        expenses_categories_collection,
        products_collection,
        product_categories_collection,
        sales_transactions_collection,
    )

    if err:
        return None, err

    return selected_collections_df, err


def select_data_components():
    with st.expander("Select Data"):
        st.markdown("###### Select data to analyse:")
        expenses_collection = st.checkbox("Expenses")
        expenses_categories_collection = st.checkbox("Expense Categories")
        products_collection = st.checkbox("Products")
        product_categories_collection = st.checkbox("Product Categories")
        sales_transactions_collection = st.checkbox("Sale Transactions")

        col1, col2 = st.columns([12, 3.8])
        with col1:
            confirm_selction = st.button("Confirm")

        with col2:
            if st.button("Clear Selection"):
                st.session_state.selected_collections = []
                st.rerun()

        if confirm_selction:
            selected_collections_df, err = cache_selected_collections_df(
                expenses_collection,
                expenses_categories_collection,
                products_collection,
                product_categories_collection,
                sales_transactions_collection,
            )

            if err:
                st.error(err)
            else:
                st.session_state.selected_collections = selected_collections_df
                st.markdown("###### Data in order of selection:")

                # if selected_collections_df is a list, iterate through the list and display each collection
                if isinstance(selected_collections_df, list):
                    for collection in selected_collections_df:
                        if collection.empty:
                            st.warning(f"No data found for selected data.")
                        else:
                            st.dataframe(collection.head(), use_container_width=True)
                elif selected_collections_df.empty:
                    st.warning(f"No data found for selected data.")
                else:
                    st.dataframe(
                        selected_collections_df.head(), use_container_width=True
                    )


def clear_button_components():
    clear_button = st.button("Clear Chat")
    if clear_button:
        st.session_state.messages = []
        st.rerun()


def chat_components():
    if prompt := st.chat_input(placeholder="Ask Biz a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            if ("selected_collections" in st.session_state) and (
                len(st.session_state.selected_collections) > 0
            ):
                response, valid = process_query(st.session_state.selected_collections)

                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                st.markdown(response)

                if not valid:
                    st.rerun()
            else:
                st.markdown("Please select a collection to proceed.")


def biz_main():
    button_style()

    col1, col2 = st.columns([5.87, 1])
    with col1:
        select_data_components()

    with col2:
        clear_button_components()

    # initialise session state variables
    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        st.session_state.messages = [{"role": "assistant", "content": get_greeting()}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    chat_components()
