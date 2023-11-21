import platform
import subprocess
import sys

USER_OS = platform.system()

def start_mongodb():
    """
    Start the MongoDB server based on the operating system.
    Return path of app.py
    """
    streamlit_command = "streamlit run /app/app.py"
    match USER_OS:
        case "Windows":
            mongo_command = "start mongod"
            streamlit_command = "streamlit run app\\app.py"
        case "Darwin":
            mongo_command = "brew services start mongodb-community"
        case "Linux":
            mongo_command = "sudo systemctl start mongod"
        case _:
            print(f"No automated process for starting Spendalyse with this OS: {USER_OS}\nLook at the Set Up section in the README for more details\n")
            sys.exit(1)
    
    try:
        subprocess.run(mongo_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting MongoDB: {e}")
        
    return streamlit_command


def run_streamlit_app():
    """
    Run the Streamlit app.
    """

    streamlit_command = start_mongodb()
    
    try:
        subprocess.run(streamlit_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit app: {e}")


if __name__ == "__main__":
    run_streamlit_app()
