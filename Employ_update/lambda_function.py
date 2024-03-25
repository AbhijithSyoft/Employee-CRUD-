import json
import mysql.connector

def lambda_handler(event, context):
    try: 
        # Connection to DataBase 
        cnx = mysql.connector.connect(
            host = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
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
        select_query="SELECT * FROM employee"
        cursor.execute(select_query)
        results=cursor.fetchall()
        
        
        body =event
        cursor.execute("""UPDATE employee SET name=%s, age=%s, gender=%s, phoneNo=%s, addressDetails=%s, workExperience=%s, qualificiations=%s, projects=%s, photo=%s WHERE id=%s""",
        (body['name'],body['age'],body['gender'],body['phoneNo'],json.dumps(body.get('addressDetails', {})),json.dumps(body.get('workExperience', {})),json.dumps(body.get('qualificiations', {})),json.dumps(body.get('projects', {})),body.get('photo',""),body['id'] ))
                        
        
        cnx.commit()
        return {
            'statusCode': 200,
            'message': "employee details updated successfully"
        }
      
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e),
            "message":event['body']
            
        }
    

    

