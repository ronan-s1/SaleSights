import os
import pytest
import subprocess


@pytest.fixture(scope="session", autouse=True)
def setup_script():
    # run setup_test_db.py before running any tests
    script_dir = os.path.dirname(os.path.abspath(__file__))
    set_up_test_db_file = os.path.join(
        script_dir, "tests", "test_set_up", "setup_test_db.py"
    )
    subprocess.run(["python", set_up_test_db_file], check=True)


if __name__ == "__main__":
    setup_script()
