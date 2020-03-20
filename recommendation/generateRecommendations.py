import psycopg2
import csv
from datetime import datetime

connection = psycopg2.connect(user="postgres",
                                password="root",
                                host="localhost",
                                port="5432",
                                database="OpisOp")

cursor = connection.cursor()

def run():
    content_recommendations()
    collab_recommendations()

    connection.commit()
    cursor.close()
    connection.close()

def content_recommendations():
    # SELECT cart.products_id, sessions.segment FROM cart
    # INNER JOIN sessions ON cart.sessions_profiles_id = sessions.browser_id
    # WHERE cart.products_id = '36286'
    # AND sessions.segment IS NOT NULL

def collab_recommendations():
    pass