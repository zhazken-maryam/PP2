import psycopg2

def connect():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="contacts",
        user="postgres",
        password="Asem1810"
    )
    print("CONNECTED")
    return conn