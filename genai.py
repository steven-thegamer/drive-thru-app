import google.generativeai as genai
import os
import sqlite3

db_conn = None

def initialize():
    my_api_key = "AIzaSyBj0dAZyXhbH7ZK-t2n38gzLHJCG9_rGkQ"
    os.environ["GOOGLE_API_KEY"] = my_api_key
    genai.configure(api_key=my_api_key)
    db_file = "sample.db"
    db_conn = sqlite3.connect(db_file)

