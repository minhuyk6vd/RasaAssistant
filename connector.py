import mysql.connector

# Connect to server


# # Fetch one result
# db = cur.fetchone()
# print("Current date is: {0}".format(row[0]))

# # Close connection
# cnx.close()

mydb = mysql.connector.connect(
host="127.0.0.1",
port=3306,
user="root",
password="12345678",
database="project_football_pitch")

cur = mydb.cursor()
name = 'Nam Kì Khởi Nghĩa'
sql = 'select f.* from football_pitchs f where f.name like "%{0}%" and f.user_id is not null;'.format(name)
sql1 = 'select f.* from football_pitchs f where f.street_number like "%{0}%" and f.user_id is not null;'.format(name)
sql2 = 'select p.* from products p where p.name like "%{0}%" and p.quantity > 0 ;'.format("giày")
cur.execute(sql2)
for table in cur:
    print(table[9])



