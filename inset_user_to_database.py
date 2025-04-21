import pymysql

def insert_user_info(name: str, email: str, password: str, topt: str, enc_key: str):
    connection = None
    cursor = None
    
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",  
            password="Jaishreeram@1000",  
            database="login_info"
        )
        
        
        cursor = connection.cursor()
        
        # Fixed query with proper escaping to prevent SQL injection
        query = "INSERT INTO users (Name, Email, password2, totp_secret, encryption_key) VALUES (%s, %s, %s, %s, %s)"
        values = (name, email, password, topt, enc_key)
        
        
        cursor.execute(query, values)
        
        connection.commit()
        
    except Exception as e:
        print(f"General error: {e}")
    finally:

        if cursor:

            cursor.close()
        if connection and connection.open:
            connection.close()

#insert_user_info("asfasdf", "asdfasdf", "sdfsdfasdfad", "sadfasdfsf", "sdkfaskdlfj")