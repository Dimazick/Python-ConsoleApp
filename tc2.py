#Глубокая бизнес логика
#добавление имя контакта
# РАБОТА С КОНТАКТАМИ #
def add_contact_name() -> str:
    value = input("Введите имя, фамилию нового контакта ")
    value = "Имя : " + value + "\n"
    return value
#добавление номера
def add_contact_phone_number() -> str:
    value = input("Введите телефонный номер или \"--\" для оставления этого поля пустым > ")
    if value == "--":
        value = "отсутствует"
    elif len(value) < 5:
        gett_fail_message(1, "Ошибка при записи номера телефона. Телефон не может содержать менее 5 символов.")

    value = "Телефон : " + value + "\n"

    return value

def add_contact_email()->str:
    dog = "@"
    value = input("Введите адрес электронной почты или \"--\" для оставления этого поля пустым > ")
    correct_mail = False
    while correct_mail is False:

        if value == "--":
            value = "отсутствует"
            correct_mail = True

        if dog in value:
            value += "\n"
            correct_mail = True
        value = input("Отсутствует символ @ в написании электронной почты, введите адрес без ошибок > ")

    value = "Email : " + value + "\n"
    return  value

#добавление контакта
def add_contact(path: str) -> None:
    file = open(path, 'a')
    contact = []
    try:
        valueName = add_contact_name()
        contact.append(valueName + '\n')
    except ValueError:
        gett_fail_message(1, "Ошибка при вводе имени, пробуй снова.")
        # добавить возврат в главное меню

    try:
        valuePhone = add_contact_phone_number()
        contact.append(valuePhone + '\n')
    except ValueError:
        gett_fail_message(1, "Ошибка при вводе телефона, попробуйте снова")
        # добавить возврат в главное меню
    except TypeError:
        gett_fail_message(1, "введите номер телефона без ошибок")


    try:
        valueMail = add_contact_email()
        contact.append(valueMail + '\n')
    except ValueError:
        gett_fail_message(1, "Ошибка при вводе электронной почты, попробуйте снова")
        # добавить возврат в главное меню

    file.write(' '.join(contact))
    file.close()
#спецфункция, для выбора функций
def get_command(path:str):
    print("Введите команду: для просмотра доступных команд наберите *help* ")
    command = input(">> ")
    match command:
        case "add": add_contact(path)
        case "read": read_contacts(path)
        case "find":
            id_find_contacts = input_find_contact(path)

            try:
                print("Какие наши дальнейшие действия?")
                exclusive_command = input(">>")
                match exclusive_command:
                    case "del":
                        id_find_contacts = whitch_will_del(id_find_contacts)
                        dellete_some_contact(path, id_find_contacts)

                    case "redact":
                        pass
                    case "exit":
                        pass
                    case "main":
                        pass
                    case "help":
                        pass


            except:
                gett_fail_message(2, "Что-то пошло не по плану")



#спецфункция для спецошибок
def gett_fail_message(type_of_message:int, message:str):
    match type_of_message:
        case 1: print("\*** Ошибка ввода ***/")
        case 2: print("\*** Логическая ошибка ***/")
        case _: print("\*** Лютейшая ошибка, даже не знаю что ты сделал ***/")
    print(message)

#функция вывода адресной книги
def read_contacts(path)->None:
    matrix = matrix_from_file(path)
    for i in range(len(matrix)):
        print(f"  {i + 1}:")
        for j in range(len(matrix[i])):
            print("".join(matrix[i][j]), end = '')

#массив из файла
def list_from_file(path):
    file = open(path, 'r')
    lst = []
    for buff in file.readlines():
        cont = buff.split(' ')
        lst.append(cont)
    file.close()
    return lst

def matrix_from_file(path):
    lst = list_from_file(path)
    buffer_list = []
    matr = []

    for i in range(len(lst)-1):
        a = lst[i]
        b = lst[i+1]
        if a == ['\n'] and b == ['\n']:

            matr.append(buffer_list)
            buffer_list = []
        else:
            buffer_list.append(a)
    return matr



#удаление контакта
def input_find_contact(path):
    try:
        find_contact = input("Мы будем искать >> ")
        if is_find_contact_in_list(path, find_contact):
            id_finders = get_find_contact_index(path, find_contact)
            print_find_contacts(path, id_finders)
            return id_finders
        else:
            gett_fail_message(2, "Искомые данные отсутствуют в файле")
            return None

    except:
        gett_fail_message(3, "")
    return None

def is_find_contact_in_list(path, find_contact)->bool:
    lst = list_from_file(path)
    string = ''
    find_contact = find_contact.lower()
    for elem in lst:
        string += str(elem).lower()
    return True if find_contact in string else False

#найдем индексы запрашиваемых контактов
def get_find_contact_index(path, find_contact:str):
    matrix = matrix_from_file(path)
    id_finders = []
    find_contact = find_contact.lower()
    if is_find_contact_in_list(path, find_contact):
        for i in range(0, len(matrix)):
            buff_string = " ".join(map(str, matrix[i])).lower()
            if find_contact in buff_string:
                id_finders.append(i)
    else:
        print("Запрашиваемые данные не найдены.")
        return None
    return id_finders

#печать найденных контактов
def print_find_contacts(path, id_finders):
    matrix = matrix_from_file(path)
    print("Найденные по вашему запросу контакты: ")
    for i in range(len(id_finders)):
        print(f"  {i + 1}:")
        for j in range(len(matrix[i])):
            print("".join(matrix[id_finders[i]][j]), end = '')
    get_command()

#сколько будем удалять?
def whitch_will_del(id_finders):
    print("Введите номер контакта, который будем удалять.")
    print("Либо напишите ALL для удаления всех найденныйх контактов ")
    target = input(">> ")
    if target.isdigit():
        target = int(target)
        if target <= len(id_finders):
            return id_finders[target+1]
        else:
            gett_fail_message(1, "Вы ввели слишком большое число")
            whitch_will_del(id_finders)
    else:
        target.lower()
        if target == "all":
            return id_finders
        else:
            gett_fail_message(2, "Некорректная команда")



#удаление контактов
def dellete_some_contact(path, id_finders):
    id_to_dell = whitch_will_del(id_finders)
    lst = list_from_file(path)
    lst = [i for j, i in enumerate(lst) if j not in id_to_dell]
    write_file_from_list(path, lst)
    print("Контакт(ы) удален")



#перезапись списка
def write_file_from_list(path, lst):
    file = open(path, "w")
    buffer_lst = []
    for element in lst:
        buffer_lst.append(element)
    for n_element in buffer_lst:
        file.write(n_element)
    file.close()









papapa = "PhoneBook"


list=[]
file=open(papapa, "r")
for byte in file.readlines():
    print(byte)
print(list)