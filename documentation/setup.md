# SaleSights Setup

- [Run Locally 🚀](#run-locally-)
  - [MongoDB](#mongodb)
    - [macOS (brew)](#macos-brew)
    - [Windows](#windows)
    - [Linux](#linux)
  - [Run Application](#run-application)
- [Run using Docker 🐋](#run-using-docker-)
- [Use Sample Data 📂](#use-sample-data-)
  - [Local](#local)
  - [Docker](#docker)

## Run Locally 🚀

To run the app locally you just need a MongoDB server and the streamlit app running.

**Python 3.10 or above**: You can download Python from [python.org](https://www.python.org/downloads/).

### MongoDB

#### macOS (brew) 
If you are using macOS and have Homebrew installed, you should install MongoDB using the following command:
```bash
brew tap mongodb/brew
brew install mongodb-community
```

#### Windows
For Windows users, MongoDB can be installed by downloading the installer from the [MongoDB website](https://www.mongodb.com/try/download/community).

#### Linux
- For Debian/Ubuntu-based systems:<br><br>
    ```bash
    sudo apt-get update
    sudo apt-get install -y mongodb
    sudo systemctl start mongod
    ```

- For Red Hat/Fedora-based systems:  
    ```bash
    sudo yum install -y mongodb
    sudo systemctl start mongod
    ```

**Note:**
If you plan to run `launch.py`, please make sure you have MongoDB installed using the appropriate method mentioned above, as this script relies on a MongoDB server for its functionality.

### Run Application

1. Clone the repo

2. Navigate to the project directory

3. Install required packages
    ```
    pip install -r requirements.txt
    ```

4. Create a `.streamlit/secrets.toml`
    ```toml
    [mongo]
    host = "localhost"
    port = 27017
    ```

6. run `launch_app.py`

## Run using Docker 🐋

1. Clone the repo

2. Navigate to the project directory

3. Create a `.streamlit/secrets.toml`
    ```toml
    [mongo]
    host = "mongo"
    port = 27017
    ```

4. Build images
    ```
    docker-compose build
    ```

5. Run containers
    ```
    docker-compose up
    ```

## Use Sample Data 📂

SaleSight's comes with sample data which you can use for testing. 

### Local
1. Run `populate/populate.py`
    ```bash
    python populate/populate.py
    ```

### Docker
1. Run containers in background
    ```bash
    docker-compose up -d
    ```

2. After containers are running, populate the database
    ```bash
   docker-compose exec streamlit-app python populate/populate.py
    ```

