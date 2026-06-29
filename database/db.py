import psycopg2

def get_connection():

    return psycopg2.connect(
        host="localhost",
        database="exchange_sim",
        user="postgres",
        password="password"
    )