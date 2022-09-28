import attendance
import pysftp
import os
import MySQLdb
import database

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

remote_dir = '/var/tmp/csv_files'
local_dir = 'csv_files'

# Get data from AWS Machine
with pysftp.Connection(host='185.164.16.144', username='avielk', password='123456',cnopts=cnopts) as sftp:
    for entry in sftp.listdir_attr(remote_dir):
        remotepath = remote_dir + "/" + entry.filename
        localpath = os.path.join(local_dir, entry.filename)
        sftp.get(remotepath, localpath)

# Apply Attendance script I coded in ex3 on the data
num_of_meetings = attendance.main_function('.')
# add the DB with the result
database.fill_data_base(num_of_meetings)
conn = MySQLdb.connect("database", "root", "123456", "avield")

def frontend_response():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    data = cursor.fetchall()  # data from database
    return data, num_of_meetings