import csv   #csv нужен для чтения CSV-файла.
from connect import connect   #имя файла connect.py, второе это функция внутри него


def create_table():
    conn = connect() #программа подключается к базе данных
    cur = conn.cursor() #и создает курсор для выполнения скл запросов

    #execute() отправляет SQL-запрос в базу данных для выполнения.
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)

    conn.commit() #сохраняет изменения
    cur.close() #закрываю курсор
    conn.close() #закрываю соединение
    print("Table created") #просто иниформация о том что таблтца создана


def insert_console():

    #дальше пользователь просто вводит имя и номер с клавиатуры
    name = input("Name: ") 
    phone = input("Phone: ")

    #опять подключаемся к базе данных и создаем курсор для выполнения скл запросов
    conn = connect() 
    cur = conn.cursor()

    #данные добавляются в таблицу с помощью скл запроса INSERT. %s — это как пустое место, куда потом вставляется значение.
    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    #сохраняем через коммит и закрываем курсор и соединение
    conn.commit()
    cur.close()
    conn.close()
    print("Inserted") #просто инфа о том что мы добавили


def insert_csv(filename):

    #подключаемся к базе данных и создаем курсор для выполнения скл запросов
    conn = connect()
    cur = conn.cursor()


    with open(filename, "r", encoding="utf-8") as file: #открывает csv файл. UTF-8 — это стандартная кодировка, которая поддерживает разные символы, например кириллицу.
        reader = csv.reader(file) #читает файл построчно
        next(reader, None) #читает файл, но пропускает первую строку

        for row in reader:
            if len(row) >= 2: #Потом программа проходит по строкам файла и проверяет, что в строке есть хотя бы 2 значения.
                #После этого имя и телефон из CSV добавляются в таблицу.
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                    (row[0], row[1])
                )

    #сохраняем и закрываем
    conn.commit()
    cur.close()
    conn.close()
    print("CSV inserted")


def update_name(old, new):
    conn = connect()
    cur = conn.cursor()

    #Эта функция изменяет имя контакта: старое имя заменяется на новое.
    cur.execute(
        "UPDATE phonebook SET first_name=%s WHERE first_name=%s",
        (new, old)
    )

    conn.commit() #сохраняем

    if cur.rowcount == 0: #rowcount показывает, была ли изменена хотя бы одна строка. Если нет, значит такого контакта нет.
        print("No such contact")
    else:
        print("Name updated")

    cur.close()
    conn.close()


def update_phone(name, new_phone):
    conn = connect()
    cur = conn.cursor()

    #Эта функция изменяет номер телефона у контакта, найденного по имени.
    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE first_name=%s",
        (new_phone, name)
    )

    conn.commit()

    if cur.rowcount == 0:
        print("No such contact")
    else:
        print("Phone updated")

    cur.close()
    conn.close()


def show_all():
    conn = connect()
    cur = conn.cursor()

    #Здесь выполняется запрос SELECT, который получает все записи из таблицы.
    #fetchall() возвращает все строки результата.
    cur.execute("SELECT * FROM phonebook") 
    rows = cur.fetchall()

    #Потом программа выводит все записи.
    for row in rows:
        print(row) 

    cur.close()
    conn.close()


def find_by_name(name):
    conn = connect()
    cur = conn.cursor()

    #ищет контакты по имени
    cur.execute("SELECT * FROM phonebook WHERE first_name=%s", (name,))
    rows = cur.fetchall() #fetchall() возвращает все строки результата.
    print(rows) 

    cur.close()
    conn.close()


def find_by_prefix(prefix):
    conn = connect()
    cur = conn.cursor()

    #Эта функция ищет номера по префиксу, то есть по началу номера. % в SQL означает любое продолжение строки.
    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + "%",)
    )

    rows = cur.fetchall() #fetchall() возвращает все строки результата.
    print(rows)

    cur.close()
    conn.close()


def delete_by_name(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE first_name=%s", (name,))
    conn.commit()

    if cur.rowcount == 0:
        print("No such contact")
    else:
        print("Deleted by name")

    cur.close()
    conn.close()


def delete_by_phone(phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()

    if cur.rowcount == 0:
        print("No such contact")
    else:
        print("Deleted by phone")

    cur.close()
    conn.close()


def menu():
    while True: #Здесь создаётся бесконечный цикл, чтобы меню работало постоянно, пока пользователь не выберет выход.
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert from console")
        print("3. Insert from CSV")
        print("4. Update name")
        print("5. Update phone")
        print("6. Show all")
        print("7. Find by name")
        print("8. Find by phone prefix")
        print("9. Delete by name")
        print("10. Delete by phone")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_console()
        elif choice == "3":
            filename = input("CSV filename: ")
            insert_csv(filename)
        elif choice == "4":
            old = input("Old name: ")
            new = input("New name: ")
            update_name(old, new)
        elif choice == "5":
            name = input("Name: ")
            new_phone = input("New phone: ")
            update_phone(name, new_phone)
        elif choice == "6":
            show_all()
        elif choice == "7":
            name = input("Name: ")
            find_by_name(name)
        elif choice == "8":
            prefix = input("Prefix: ")
            find_by_prefix(prefix)
        elif choice == "9":
            name = input("Name: ")
            delete_by_name(name)
        elif choice == "10":
            phone = input("Phone: ")
            delete_by_phone(phone)
        elif choice == "0":
            print("Bye")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu() #Если файл запускается напрямую, тогда запускается функция menu(), и программа начинает работать через меню.