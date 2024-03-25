import json
import mysql.connector

def lambda_handler(event, context):
    try: 
        # Connection to DataBase 
        cnx = mysql.connector.connect(
            host = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            user = "admin",
            password = "asdfghjkl",
            database="mydatabase")
        cursor=cnx.cursor()
        
        # CREATEING DATABASE
        # create_db_query = "CREATE DATABASE IF NOT EXISTS mydatabase"
        # cursor.execute(create_db_query)
        
        # Checking for table
        table_exits_query='SHOW TABLES LIKE "employee"'
        cursor.execute(table_exits_query)
        table_exists=cursor.fetchone()
    
        # Creating table  if not exist
        if not table_exists:
            create_table_query="""
                    CREATE TABLE IF NOT EXISTS employee (
                        id  CHAR(10) PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        age INT NOT NULL,
                        gender VARCHAR(10) NOT NULL,
                        phoneNo VARCHAR(20) ,
                        addressDetails JSON,
                        workExperience JSON ,
                        qualificiations JSON,
                        projects JSON,
                        photo VARCHAR(255)
                    )
                """
            cursor.execute(create_table_query)
            cnx.commit()
            
        user_id = event.get('user_id')
        if user_id is None:
            return {
                'statusCode': 400,
                'message': 'User ID is missing in the request'
            }
        
        id_is_exists = f"SELECT COUNT(*) AS employee_count FROM employee WHERE id = '{user_id}' ;"
        cursor.execute(id_is_exists)
        results = cursor.fetchone()
        if results[0] == 0:
            return {
                'statusCode': 400,
                'message': 'User ID does not exist'
            }


        
        user_id =event['user_id']
        cursor.execute("DELETE FROM employee WHERE id=%s", (user_id,))
        cnx.commit()
        cursor.close()
        cnx.close()
        return {
                    'status code': 200,
                    'body': "employee deleted successfully"
                }
      
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(event)),
            "message":str(e)
        }
