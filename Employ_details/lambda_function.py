import json
import mysql.connector

def lambda_handler(event, context):
    try: 
        # Connection to DataBase 
        cnx = mysql.connector.connect(
            host = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
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
    
        # Geting all employee details
        select_query="SELECT * FROM employee;"
        cursor.execute(select_query)
        results=cursor.fetchall() 
        
        
        
        table_data=[]
        for row in results:
            table_data.append({
                "id":row[0],
                "name":row[1],
                "email":row[2],
                "age":row[3],
                "gender":row[4],
                "phoneNo":row[5],
                "addressDetails":row[6],
                "workExperience":row[7],
                "qualificiations":row[8],
                "projects":row[9],
                "photo":row[10]}
                )
        cursor.close()
        cnx.close()
        return {
                "status code": 200,
                "message": "employee Details",
                "data": table_data
            }
      
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
    

    

