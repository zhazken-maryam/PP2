import psycopg2 #библиотека которая поможет нам соединить пайтон с постгрескл и пользоваться командами скл

def connect(): #создаем функцию которая поможет нам возвращать подключение к нашей базе 
    conn = psycopg2.connect( #это попытка установить соединение с PostgreSQL
        host="localhost", 
        port=5432, 
        database="contacts", #к какой базе подключаемся
        user="postgres", #пользователь
        password="Asem1810" #пароль
    )
    print("CONNECTED") #просто говорит что соединено
    return conn #возвращает conn