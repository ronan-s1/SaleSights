# SaleSights Setup

## Run Locally 🖥️

To run the app locally you need a MongoDB server and the Streamlit application running. It is recommend to use Python 3.10 for optimal compatibility.

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
- For Debian/Ubuntu-based systems:
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

4. run `launch_app.py`

5. Got to http://127.0.0.1:8501/

## Run using Docker 🐋

1. Clone the repo

2. Navigate to the project directory

3. Build images
    ```bash
    docker-compose build
    ```

4. Run containers
    ```bash
    docker-compose up
    ```

5. Go to http://127.0.0.1:8501/

## Use Sample Data 📂

SaleSight's comes with sample data which you can use for testing. 

### Local
1. Run `populate/populate.py`
    ```bash
    python populate/populate.py
    ```

### Docker
1. Run containers in the background
    ```bash
    docker-compose up -d
    ```

2. After the containers are running, populate the database
    ```bash
   docker-compose exec streamlit-app python populate/populate.py
    ```

    