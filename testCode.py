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

        elif dog in value:
            value += "\n"
            correct_mail = True
        else:
            print("Отсутствует символ @ в написании электронной почты, введите адрес без ошибок > ")
            value = add_contact_email()

    value = "Email : " + value + "\n"
    return value

#добавление контакта
def add_contact(path: str) -> None:
    file = open(path, 'a')
    contact = []
    terminator = "*****"
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
    contact.append(terminator + '\n')
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
            find_contact = input_find_contact()
            try:
                if is_find_contact_in_list(path, find_contact):
                    id_find_contacts = get_find_contact_index(path, find_contact)
                    print_find_contacts(path, id_find_contacts)
                    print("Какие наши дальнейшие действия?")
                    exclusive_command = input(">>")
                    match exclusive_command:
                        case "del":
                            dellete_some_contact(path, id_find_contacts)
                            print("Книга после удаленияконтакта(ов) :")
                            read_contacts(path)

                        case "redact":
                            pass
                        case "exit":
                            pass
                        case "main":
                            pass
                        case "help":
                            pass


            except ValueError:
                gett_fail_message(2, "Что-то пошло не по плану")
            except ZeroDivisionError:
                gett_fail_message(2, "Что-то пошло не по плану zero")



#спецфункция для спецошибок
def gett_fail_message(type_of_message:int, message:str):
    match type_of_message:
        case 1: print("\*** Ошибка ввода ***/")
        case 2: print("\*** Логическая ошибка ***/")
        case _: print("\*** Лютейшая ошибка, даже не знаю что ты сделал ***/")
    print(message)

#функция вывода адресной книги
def read_contacts(path)->None:
    matrix = get_matrix_from_file(path)
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

def get_matrix_from_file(path):
    buffer_list = []
    matrix = []
    terminator = "****"
    file = open(path, 'r')
    for buff in file.readlines():
        buffer_list.append(buff)
        if terminator in buff:
            matrix.append(buffer_list)
            buffer_list = []
    return matrix



#удаление контакта
def input_find_contact():
    try:
        find_contact = input("Мы будем искать >> ")
        return find_contact
    except ValueError:
        gett_fail_message(2, "Пробуй еще раз")
        #добавить доработтаную гет команд
        pass


def is_find_contact_in_list(path, find_contact)->bool:
    lst = list_from_file(path)
    string = ''
    find_contact = find_contact.lower()
    for elem in lst:
        string += str(elem).lower()
    return True if find_contact in string else False

#найдем индексы запрашиваемых контактов
def get_find_contact_index(path, find_contact:str):
    matrix = get_matrix_from_file(path)
    id_finders = []
    find_contact = find_contact.lower()
    for i in range(0, len(matrix)):
        buff_string = " ".join(map(str, matrix[i])).lower()
        if find_contact in buff_string:
            id_finders.append(i)
    return id_finders


#лист удаляемых контактов
def get_del_contacts_list(path, id_finders):
    lst = get_matrix_from_file(path)
    del_cont_matrix = lst[id_finders]
    return del_cont_matrix

#печать найденных контактов
def print_find_contacts(path, id_finders):
    matrix = get_matrix_from_file(path)
    print("Найденные по вашему запросу контакты: ")
    for i in range(len(id_finders)):
        print(f"  {i + 1}:")
        for j in range(len(matrix[i])):
            print("".join(matrix[id_finders[i]][j]), end = '')


#сколько будем удалять?
def whitch_will_del(id_finders):
    print("Введите номер контакта, который будем удалять.")
    print("Либо напишите ALL для удаления всех найденныйх контактов ")
    id_to_del = []
    target = input(">> ")
    if target.isdigit():
        target = int(target)
        length_of_finds = len(id_finders)
        if target <= length_of_finds:
            id_to_del.append(id_finders[target-1])
            return id_to_del
        else:
            gett_fail_message(1, "Вы ввели слишком большое число")
            whitch_will_del(id_finders)
    else:
        target = target.lower()
        if target == "all":
            return id_finders
        else:
            gett_fail_message(2, "Некорректная команда")
            #добавить выход в меню



#удаление контактов
def dellete_some_contact(path, id_finders):
    id_to_dell = whitch_will_del(id_finders)
    matrix = get_matrix_from_file(path)
    new_matrix=[]
    for i in range(len(matrix)):
        for j in range(len(id_to_dell)):
            if i != id_to_dell[j]:
                new_matrix.append(matrix[i])

    write_file_from_list(path, new_matrix)
    print("Контакт(ы) удален")



#перезапись списка
def write_file_from_list(path, lst):
    file = open(path, "w")
    buffer_lst = []
    for contact in lst:
        for string in contact:
            buffer_lst.append("".join(string))


    for n_element in buffer_lst:
        file.write(n_element)
    file.close()








newPath = "PhoneBook.txt"


get_command(newPath)
