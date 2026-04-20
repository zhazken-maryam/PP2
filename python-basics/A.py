import psycopg2  #библиотека для работы с postgresql
from config import load_config #импортирует код из congig которые дает параметры подключения


def connect(): #создаем функцию подключения к базе
    try: #тут блок где может быть ошибка
        config = load_config() #получаем настройки из config типа host db user password
        conn = psycopg2.connect(**config) #подключаемся к базе. **config-распаковка словаря
        print('Connected to the PostgreSQL server.') 
        return conn #возвращаем соединение
    except (psycopg2.DatabaseError, Exception) as error: #На случай если ошибка подключения:
        print(error) 
        return None #вывожу ошибку и возвращаем None


if __name__ == '__main__':  #если файл запускается напрямую:
    conn = connect() #пробуем подключиться
    if conn is not None: #если получилось то закрываем соединение
        conn.close()