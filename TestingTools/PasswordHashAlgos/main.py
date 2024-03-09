import pymysql
from argon2 import PasswordHasher
hasher = PasswordHasher()
conn = pymysql.Connect(host="db-itfest2024.a.aivencloud.com",
                user="avnadmin",
                port=23532,
                password="AVNS_GcjwTb1VbaBDbhRn24R",
                database="defaultdb")
cursor = conn.cursor()
print(len(hasher.hash(password="admin")))
cursor.execute("INSERT INTO `users` (`username`,`password`,`admin`) VALUES (%s,%s,%s)",
               ('admin',hasher.hash(password="admin"),1))
conn.commit()
cursor.execute("SELECT * FROM `users`")
res = cursor.fetchone()
print(res)
print(hasher.verify(res[2],password="admin"))