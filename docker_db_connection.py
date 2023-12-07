import os
import textwrap


def is_running_in_docker():
    """
    Check if the script is running inside a Docker container.

    Returns:
        bool: True if running in Docker, False otherwise.
    """
    path = "/proc/self/cgroup"
    return (
        os.path.exists("/.dockerenv")
        or os.path.isfile(path)
        and any("docker" in line for line in open(path))
    )


def update_secrets_file():
    """
    Update the secrets file based on the environment (Docker or local).

    Prints:
        str: A message indicating whether the secrets file was updated for Docker or local environment.

    Returns:
        None
    """
    secrets_path = os.path.join(".streamlit", "secrets.toml")

    if is_running_in_docker():
        secrets_content = textwrap.dedent(
            """
            [mongo]
            host = "mongo"
            port = 27017
            """
        )
        print("Secrets file updated for Docker env.")
    else:
        secrets_content = textwrap.dedent(
            """
            [mongo]
            host = "localhost"
            port = 27017
            """
        )
        print("Secrets file updated for local env.")

    with open(secrets_path, "w") as secrets_file:
        secrets_file.write(secrets_content)


if __name__ == "__main__":
    update_secrets_file()
