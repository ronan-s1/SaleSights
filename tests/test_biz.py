import switch_path
import pytest
import pandas as pd
from biz.biz_controller import (
    process_query,
    selected_collections_processing,
    get_prefix_suffix,
)
from biz.utils.prompt_templates import (
    SINGLE_DF_PREFIX,
    SINGLE_DF_SUFFIX,
    MULTI_DF_PREFIX,
    MULTI_DF_SUFFIX,
)


def test_process_query():
    # Test when an empty dataframe is passed
    result, valid = process_query(pd.DataFrame())
    assert result == "Please select valid data to proceed. (single df is empty)"
    assert valid is False

    # Test when a list of empty dataframes is passed
    result, valid = process_query([pd.DataFrame(), pd.DataFrame()])
    assert (
        result
        == "Please select valid data to proceed. (multiple df selected but all empty)"
    )
    assert valid is False

    # Test when invalid data is passed
    result, valid = process_query("invalid data")
    assert result == "Please select valid data to proceed. (data not a df or list)"
    assert valid is False


def test_selected_collections_processing():
    # Test when no collection is selected
    selected_collections = []
    result, valid = selected_collections_processing(selected_collections)
    assert result is None
    assert valid == "Please select valid data to proceed."

    # Test when only one collection is selected
    selected_collections = ["collection1"]
    result, valid = selected_collections_processing(selected_collections)
    assert result == "collection1"
    assert valid is None

    # Test when multiple collections are selected
    selected_collections = ["collection1", "collection2", "collection3"]
    result, valid = selected_collections_processing(selected_collections)
    assert result == ["collection1", "collection2", "collection3"]


def test_get_prefix_suffix():
    # Test when a single dataframe is passed
    selected_collections_df = pd.DataFrame()
    prefix, suffix = get_prefix_suffix(selected_collections_df)
    assert prefix == SINGLE_DF_PREFIX
    assert suffix == SINGLE_DF_SUFFIX

    # Test when a list of multiple dataframes is passed
    selected_collections_df = [pd.DataFrame(), pd.DataFrame()]
    prefix, suffix = get_prefix_suffix(selected_collections_df)
    assert prefix == MULTI_DF_PREFIX
    assert suffix == MULTI_DF_SUFFIX

    # Test when invalid data is passed
    selected_collections_df = "invalid data"
    prefix, suffix = get_prefix_suffix(selected_collections_df)
    assert prefix == SINGLE_DF_PREFIX
    assert suffix == SINGLE_DF_SUFFIX


if __name__ == "__main__":
    pytest.main(["-v", __file__])
