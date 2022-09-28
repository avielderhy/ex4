import pandas as pd
import MySQLdb


def fill_data_base(num_of_meetings):
    data = pd.read_csv('results.csv', encoding="utf-8", sep="\t")
    conn = MySQLdb.connect(host='database', database='avield', user='root', password='123456', auth_plugin="mysql_native_password")
    cursor = conn.cursor()
    cursor.execute("select database();")
    cursor.execute('DROP TABLE IF EXISTS attendance;')
    command = "CREATE TABLE `attendance` (Email varchar(255),Name varchar(255),"
    for i in range(num_of_meetings):
        command += f"Meeting_{i+1} varchar(255), "
    command = command[:-2] + ")"
    cursor.execute(command)

    for i, row in data.iterrows():
        real_row = str(str(tuple(row)[0]).split(","))[1:]
        real_row = real_row[:-1]
        sql = f"INSERT INTO `attendance` VALUES ({real_row});"
        cursor.execute(sql)
        conn.commit()
