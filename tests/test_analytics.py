import switch_path
from datetime import datetime
import pytest
from analytics.analytic_controller import format_date
from analytics.analytic_data import fetch_expenses_by_day_of_week


def test_format_date():
    # Test formatting of start and end date
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 1, 31)
    start_date_str, end_date_str = format_date(start_date, end_date)
    assert start_date_str == "2022-01-01"
    assert end_date_str == "2022-01-31"


if __name__ == "__main__":
    pytest.main()
