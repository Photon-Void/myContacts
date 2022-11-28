import pickle, os


def write_data(dbPath, db):
    with open(dbPath, 'wb') as file:
        pickle.dump(db, file)


def connect_db(dbPath: str) -> list[dict]:
    '''
    Возращает данные бд, если она существует.
    Создает бд и возращает данные, если её нет

    Args:
        dbPath (str): путь к бд.

    Returns:
        list[dict]: данные.

    '''
    # создать каталог, если отсутствует
    if not os.path.exists('database'):
        os.mkdir('database')
    # создать бд, если нет
    if not os.path.exists(dbPath):
        db = [{
            'name':'', 'phone':'',
            'email':'', 'desc':''}
            ]
        write_data(dbPath, db)
    # чтение данных
    with open(dbPath, 'rb') as file:
        db = pickle.load(file)

    return db


def show_contact(db: list[dict]):
    '''
    Показывает контакт(ы).

    Args:
        db (list[dict]): База данных.

    Returns:
        None.

    '''
    print("\n<Показ контакта>")
    print("[*] - вывести все контакты")
    print("[имя_контакта] - вывести определённый(ые) контакт(ы)")

    contact = input(">>> ").capitalize()
    print("индекс | имя_контакта(0) | номер_телефона(1) | почта(2) | описание(3)\n")
    for i in range(1, len(db)):
        if contact == '*' or db[i]['name'].startswith(contact):
            prt = f"{i} | {db[i]['name']} | {db[i]['phone']} | \
                {db[i]['email']} | {db[i]['desc']}"

            print(prt)


def add_contact(dbPath: str, db: list[dict]):
    '''
    Добавляет новый контакт в бд и вызывает write_data().

    Args:
        dbPath (str): Путь к бд. Передается в write_data.
        db (list[dict]): База данных. Передается в write_data.

    Returns:
        None.

    '''
    # ввод нового контакта
    print("\n<Добавление контакта>")
    name = input("Введите имя(Enter для отмены)\n>>> ").capitalize()
    phone = input("Введите номер телефона(Enter для отмены)\n>>> ")
    email = input("Введите почту(не обезательно)\n>>> ")
    desc = input("Введите рписание(не обезательно)\n>>> ")
    d = {
        'name': name, 'phone': phone,
        'email': email, 'desc': desc
        }

    if not d['name'] and not d['phone']:
        print("Отмена. Возрат в главное меню...\n")
    else:
        # изначально бд содержит {key: ''}
        # данные хранятся в сортированом виде
        if (len(db) == 1) or (db[-1]['name'] <= d['name']):
            db.append(d)
        else:
            for i in range(1, len(db)):
                if db[i-1]['name'] <= d['name'] <= db[-1]['name']:
                    db.insert(i, d)
                    break
        # запись
        write_data(dbPath, db)
        print(f"\nКонтакт {d['name']} добавлен.")


def del_contact(dbPath, db):
    print("\n<Удаление контакта>")
    show_contact(db)
    contactIdx = int(input("Индекс конатакта или Enter для отмены\n>>> "))
    if not contactIdx and contactIdx == 0:
        print("Отмена. Возрат в главное меню...\n")
    else:
        del db[contactIdx]
        write_data(dbPath, db)
        print("Контакт удалён.\n")


def edit_contact(dbPath: str, db: list[dict]):
    '''
    Редактирует контант.

    Args:
        dbPath (str): пусть к бд.
        db (list[dict]): База данных.

    Returns:
        None.

    '''
    keys = {'0': 'name', '1': 'phone', '2': 'email', '3': 'desc'}
    show_contact(db)
    try:
        row, col, new_value = input('row, col, new_value\n>>> ').split()
        row = int(row)
        db[row][keys[col]] = new_value
    except ValueError:
        print("<Ошибка> 1-ый и 2-ой параметры должи быть числами.\
              Кол-во параметров должно быть = 3.\n")
    except KeyError:
        print("<Ошибка> Неправильный 2-ой параметр(цифра в скобках).\n")
    else:
        write_data(dbPath, db)
        print("<Успех> Контакт отредактирован.\n")


def show_menu():
    commands = {
        '1': "вывод",
        '2': "добавить",
        '3': "удалить",
        '4': "редактировать",
        '0': "выход"
        }
    print()
    for i in commands:
        print(f"{i}: {commands[i]}")


def main():
    dbPath = 'database\\db.txt'
    db = connect_db(dbPath)
    # основной цикл программы
    while True:
        show_menu()

        cmd = input('>>>: ').lower()
        if cmd == '1':
            show_contact(db)
        elif cmd == '2':
            add_contact(dbPath, db)
        elif cmd == '3':
            del_contact(dbPath, db)
        elif cmd == '4':
            edit_contact(dbPath, db)
        elif cmd == '0':
            break
        else:
            print("Неверная комманда.")
        print('-'*30)


    input("Для выхода нажмите любую клавишу.")


if __name__ == '__main__':
    main()