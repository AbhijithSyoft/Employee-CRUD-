import json
import mysql.connector

def lambda_handler(event, context):
    try: 
        # Connection to DataBase 
        cnx = mysql.connector.connect(
            host = "xxxxxxxxxxxxxxxxxxxx",
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
        

        select_data="SELECT id FROM employee ORDER BY id DESC LIMIT 1"
        cursor.execute(select_data)
        results_data=cursor.fetchone()
        last_two_digits = int(str(results_data[0])[-2:]) + 1
        formatted_value = f"EMP{str(last_two_digits).zfill(2)}"
        
       
        
        body =event
        email_checking = f"SELECT COUNT(*) AS email_count FROM employee WHERE email = '{body['email']}' ;"
        cursor.execute(email_checking)
        email_result = cursor.fetchone()
        if email_result and email_result[0] > 0:
            return {
                'status code': 400,
                'message': 'This email already exists, please try another email'
            }
            
        
        insert_data = f"""INSERT INTO employee (id, name, email, age, gender, phoneNo, addressDetails, workExperience, qualificiations, projects, photo) 
                        VALUES ('{formatted_value}', '{body['name']}', '{body['email']}', {body['age']}, '{body['gender']}', '{body['phoneNo']}', '{json.dumps(body.get('addressDetails', []))}', '{json.dumps(body.get('workExperience', []))}', '{json.dumps(body.get('qualificiations', []))}', '{json.dumps(body.get('projects', []))}', {'NULL' if body.get('photo') is None else "'" + body['photo'] + "'"})"""
        cursor.execute(insert_data)
        cnx.commit()
        return {
            'status code': 200,
            'message':'employee created successfully',
            'regid':formatted_value
        }
      
    except Exception as e:
        return {
            'status code': 500,
            'message': str(e),
            "error":str(e)
            
        }
    
