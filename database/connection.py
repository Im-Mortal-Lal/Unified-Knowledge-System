import pyodbc

from config import SERVER, DATABASE, DRIVER


def get_connection():

    connection = pyodbc.connect(

        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
    )

    return connection