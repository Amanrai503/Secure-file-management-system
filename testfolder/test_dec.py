import mysql.connector
def insert_user(name: str, email: str, password: str, key: str):
        print(name, email, password, key)
        try:
            connection =mysql.connector.connect(
                host="localhost",
                user="root",  
                password="1234",  
                database="login_info"
            )
            cursor = connection.cursor()
            query = "INSERT INTO users (Name, Email, password2, totp_secret) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, password, key))
            connection.commit()
            print("User inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        print("done//////////////////////")

insert_user("Aman", "example@gmail.com", "DJDKLSIJJDD", "1234567890")