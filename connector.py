import mysql.connector

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

sql5 = 'SELECT f.* FROM football_pitchs f \
                inner join wards w on f.ward_id = w.id \
                inner join districts d on w.district_id=d.id \
                where (d.district_name like "%{0}%" or w.ward_name like "%{0}%" or f.street_number like "%{0}%") and f.user_id is not null;'.format(name)


cur.execute(sql5)
for table in cur:
    print(table[7])



