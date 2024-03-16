import textwrap
import os
import subprocess
from populate_test import populate


def mongo_config():
    # Set up the secrets file for the MongoDB connection
    secrets_path = os.path.join(".streamlit", "secrets.toml")
    with open(secrets_path, "w") as secrets_file:
        secrets_file.write(
            textwrap.dedent(
                """
                [mongo]
                host = "localhost"
                port = 27018
                """
            )
        )


def start_mongodb():
    """
    Start the MongoDB server container.
    """
    # Get the directory of the current script and the path to the docker-compose file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    compose_file_path = os.path.join(script_dir, "docker-compose.yml")

    # Check if the file exists
    if not os.path.exists(compose_file_path):
        print(f"Error: docker-compose.yml not found at {compose_file_path}")
        return

    try:
        subprocess.run(
            ["docker-compose", "-f", compose_file_path, "up", "-d"], check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error starting MongoDB with docker-compose: {e}")


if __name__ == "__main__":
    mongo_config()
    start_mongodb()
    populate()
