import psycopg2

try:
    connection = psycopg2.connect(
    host='localhost',
    user='alkymer',
    password='Alkemy22',
    database='training'
    )
    print("conexión exitosa")
    #cursor=connection.cursor()
    #cursor.execute("SELECT version()")
    #row=cursor.fetchone()
    #print(row)
    #cursor.execute("SELECT * FROM moron_nacional_pampa")
    #rows=cursor.fetchall
    #for row in rows:
    #   print(row)
except Exception as ex:
    print(ex)