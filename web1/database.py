import mysql.connector
from mysql.connector import errorcode

def connect_to_mysql():
    try:
        cnx = mysql.connector.connect(user='root', password='1412003@', host='127.0.0.1')
        print("Connected to MySQL database")

        # Tạo cơ sở dữ liệu mới nếu chưa tồn tại
        db_name = 'new_database_3'
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        cursor = cnx.cursor()
        cursor.execute(create_db_query)
        print(f"Database '{db_name}' đã được tạo hoặc tồn tại")

        # Đóng kết nối cursor sau khi hoàn thành
        cursor.close()

        # Kết nối đến cơ sở dữ liệu mới
        cnx.database = db_name
        print(f"Connected to database '{db_name}'")
        
        return cnx

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print(err)
        return None

cnx = connect_to_mysql()
