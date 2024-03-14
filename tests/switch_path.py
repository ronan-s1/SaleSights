# switch the path to the app folder so that the tests can import app modules
import sys
from os import path

sys.path.append(path.join(path.dirname(__file__), "../app/"))
