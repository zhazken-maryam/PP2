import psycopg2
from config import load_config


def connect():
    try:
        config = load_config()
        return psycopg2.connect(**config)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Connection error:", error)
        return None
