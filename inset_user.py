import mysql.connector
from mysql.connector import Error
import traceback

def insert_user_info(name: str, email: str, password: str, topt: str):
    connection = None
    cursor = None
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="1234",  
            database="login_info"
        )
        
        
        cursor = connection.cursor()
        
        # Fixed query with proper escaping to prevent SQL injection
        query = "INSERT INTO users (Name, Email, password2, totp_secret) VALUES (%s, %s, %s, %s)"
        values = (name, email, password, topt)
        
        
        cursor.execute(query, values)
        
        connection.commit()
        
    except Exception as e:
        print(f"General error: {e}")
        print(traceback.format_exc())
    finally:

        if cursor:

            cursor.close()
        if connection and connection.is_connected():
            connection.close()