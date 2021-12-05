import csv

import psycopg2
from psycopg2 import Error
try:
    # Подключение к существующей базе данных
    
    connection = psycopg2.connect(user="user",
                                  # пароль, который указали при установке PostgreSQL
                                  password="",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="routes")

#     # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()


    # with open('../data/geo_objects.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=';')
#     for row in reader:
#         print(row['Город'], row['lat'], row['lng'])
    

#     cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
# ...      (100, "abc'def"))



    with open('../data/geo_objects.csv', newline='') as csvfile:
      reader = csv.DictReader(csvfile, delimiter=';')
      for row in reader:
        insert_query = "INSERT INTO main_city (name, point_x, point_y) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (row['Город'], row['lat'], row['lng']))
        
    connection.commit()
    cursor.execute("SELECT * FROM main_city")
    records = cursor.fetchall()
    print(records)
    
    
    

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")