# Задача 38: Дополнить телефонный справочник возможностью изменения и удаления данных. 
# Пользователь также может ввести имя или фамилию, и Вы должны реализовать функционал для изменения и удаления данных


import os
import json
import uuid

ENCODING = 'UTF-8'


def delete(handbook: list) -> None:
    print('Выберите запись для удаления.')
    temp = find(handbook)
    while not len(temp) == 1:
        print('Необходимо выбрать запись справочника')
        temp = find(temp)
    contact = temp[0]
    print(f'Вы уверены, что хотите удалить запись:\n\tuuid: {contact["uuid"]}\n\tИмя: {contact["Имя"]}'
          f'\n\tФамилия: {contact["Фамилия"]}')
    if input('>>> ').lower() in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]:
        unique_identifier = handbook.pop(handbook.index(contact))['uuid']
        print(f'Запись с uuid: "{unique_identifier}"; была удалена.')


def update(handbook: list) -> None:
    print('Выберите запись для изменения.')
    temp = find(handbook)
    while not len(temp) == 1:
        print('Необходимо выбрать запись справочника')
        temp = find(temp)
    contact = temp[0]
    keys = [key for key in contact]
    local_menu = ['1. Изменить значение полей записи', '2. Добавить поля записи']
    numerated_keys_values = lambda: '\n'.join(f'{num}. {key}: {contact[key]}' for num, key in enumerate(keys, 1))
    print('Выбранный контакт:',
          numerated_keys_values(),
          'Выберете номер команды:',
          '\n'.join(command for command in local_menu),
          sep='\n'
          )
    while choice := input('>>> '):
        try:
            command_index = int(choice) - 1
            if command_index < 0 or len(local_menu) - 1 < command_index:
                raise IndexError
        except ValueError:
            print(f'Не удалось преобразовать "{choice}" к индексу команды. Повторите ввод.')
            continue
        except IndexError:
            print('Такой команды пока нет, повторите ввод.')
            continue
        else:
            if command_index == 0:
                print(f'Выберите номер поля для изменения:\n', numerated_keys_values(), sep='')
                while choice := input('>>> '):
                    try:
                        command_index = int(choice) - 1
                        if command_index < 0 or len(keys) - 1 < command_index:
                            raise IndexError
                    except ValueError:
                        print(f'Не удалось преобразовать "{choice}" к индексу команды. Повторите ввод.')
                        continue
                    except IndexError:
                        print('Такой команды пока нет, повторите ввод.')
                        continue
                    else:
                        contact[keys[command_index]] = input(f'Введите новое значение поля "{keys[command_index]}":'
                                                             f'\n>>> ')
                        print('Хотите изменить еще одно поле?')
                        if input('>>> ').lower() in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]:
                            print(f'Выберите номер поля для изменения:\n', numerated_keys_values(), sep='')
                            continue
                        else:
                            return
            elif command_index == 1:

                while (input(f'Добавить дополнительную информацию о контакте?\n>>> ').lower()
                       in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]):
                    keys = [*get_predefined_fields('other_information'), 'Пользовательское поле']
                    add_new_fields(contact, keys)

                while (input(f'Добавить номер телефона контакту?\n>>> ').lower()
                       in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]):
                    keys = [*get_predefined_fields('contact_information'), 'Пользовательское поле']
                    add_new_fields(contact, keys)

                while (input(f'Добавить адрес электронной почты контакту?\n>>> ').lower()
                       in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]):
                    keys = [*get_predefined_fields('email_address'), 'Пользовательское поле']
                    add_new_fields(contact, keys)
                return


def find_one(handbook: list, unique_identifier: str) -> list:
    found = list(filter(lambda el: el['uuid'] == unique_identifier, handbook))
    return found


def get_entries(entity: dict, substrings: tuple) -> bool:
    return set(entity.values()) > set(substrings)


def find_entries(handbook: list, *args) -> list:
    found = list(filter(lambda contact: get_entries(contact, args), handbook))
    return found


def find(handbook: list) -> list:
    local_menu = ('1. Найти по uuid', '2. Найти по совпадению подстрок')
    print('Укажите номер способа поиска:\n', '\n'.join(local_menu), sep='')
    while choice := input('>>> '):
        try:
            command_index = int(choice) - 1
            if command_index < 0 or len(local_menu) - 1 < command_index:
                raise IndexError
        except ValueError:
            print(f'Не удалось преобразовать "{choice}" к индексу команды. Повторите ввод.')
            continue
        except IndexError:
            print('Такой команды пока нет, повторите ввод.')
            continue
        else:
            if command_index == 0:
                if 1 < (length := len(handbook)):
                    print(f'Поиск ведется по {length} записям. Показать текущую группу?')
                    if input('>>> ').lower() in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]:
                        print(read(handbook))
                    condition = input('Введите uuid записи для поиска:\n>>> ')
                    return find_one(handbook, condition)
            elif command_index == 1:
                substrings = list()
                print('Укажите подстроку поиска:')
                while temp := input('>>> '):
                    substrings.append(temp)
                    if (input('Добавить еще подстроку для поиска?\n>>> ').lower()
                            in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]):
                        continue
                    break
                found = find_entries(handbook, *substrings)
                if (length := len(found)) == 1:
                    return found
                elif 1 < length:
                    print(f'Найдено {length} записей, показать?')
                    if input('>>> ').lower() in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]:
                        print(read(found))
                    print('Продолжить поиск в найденных записях?')
                    if input('>>> ').lower() in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]:
                        return find(found)
                else:
                    print('Записи удовлетворяющие условиям поиска не найдены, начать заново?')
                    if input('>>> ').lower() in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]:
                        return find(handbook)


def read(handbook: list) -> str:
    contacts_str = ''
    for num, contact in enumerate(handbook, 1):
        contacts_str += f'Контакт №{num}:\n'
        contacts_str += '\n'.join(f'\t\t\t{k}: {v}' for k, v in contact.items()) + '\n'
    return contacts_str


def get_predefined_fields(key: str) -> list:
    predefined_fields = dict(
                             main_info=[
                                        'Имя',
                                        'Фамилия'
                                       ],
                             other_information=[
                                                'Отчество',
                                                'Девичья фамилия',
                                                'Суффикс',
                                                'Псевдоним',
                                                'Компания',
                                                'Подразделение',
                                                'Должность'
                                               ],
                             contact_information=[
                                                  'Сотовый телефон',
                                                  'Домашний телефон',
                                                  'Рабочий телефон',
                                                  'Учебный телефон',
                                                  'Основной телефон',
                                                  'Домашний факс',
                                                  'Рабочий факс'
                                                 ],
                             email_address=[
                                            'Домашний email',
                                            'Рабочий email',
                                            'Учебный email',
                                            'Основной email'
                                           ]
                            )
    return predefined_fields[key]


class KeyExistsError(Exception):
    pass


def add_new_fields(contact: dict, fields_names: list) -> None:
    local_menu = '\n'.join(f'{num}. {field_name}' for num, field_name in enumerate(fields_names, 1))
    print(f'Выберите имя поля по номеру:\n{local_menu}')
    while choice := input('>>> '):
        try:
            command_index = int(choice) - 1
            if command_index < 0 or len(fields_names) - 1 < command_index:
                raise IndexError
            if (key := fields_names[command_index]) in contact:
                raise KeyExistsError
            if key in fields_names[:-1]:
                contact[key] = input(f'Укажите {key.lower()}:\n>>> ')
            else:
                key = input('Введите название пользовательского поля:\n>>> ')
                contact[key] = input(f'Укажите {key.lower()}:\n>>> ')
            return
        except ValueError:
            print(f'Не удалось преобразовать "{choice}" к индексу команды. Повторите ввод.')
            continue
        except IndexError:
            print('Такой команды пока нет, повторите ввод.')
            continue
        except KeyExistsError:
            print(f'Поле "{key}" уже было присвоено контакту.')
            continue
        except Exception as ex:
            print(f'Введено "{choice}":', ex)
            continue


def create(handbook: list) -> None:
    new_contact = dict()

    while find_entries(handbook, (new_uuid := str(uuid.uuid4()).split('-')[0],)):
        pass
    else:
        new_contact['uuid'] = new_uuid

    for field in get_predefined_fields('main_info'):
        while not (value := input(f'Введите {field.lower()}:\n>>> ')):
            print('Поле обязательно для заполнения, повторите ввод.')
        new_contact[field] = value
    main_info = f'{new_contact["Имя"]} {new_contact["Фамилия"]}'

    while (input(f'Добавить дополнительную информацию о контакте: "{main_info}"?\n>>> ').lower()
           in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]):
        keys = [*get_predefined_fields('other_information'), 'Пользовательское поле']
        add_new_fields(new_contact, keys)

    while (input(f'Добавить номер телефона контакту: "{main_info}"?\n>>> ').lower()
           in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]):
        keys = [*get_predefined_fields('contact_information'), 'Пользовательское поле']
        add_new_fields(new_contact, keys)

    while (input(f'Добавить адрес электронной почты контакту: "{main_info}"?\n>>> ').lower()
           in ['Yes'.lower(), 'Y'.lower(), 'Да'.lower(), 'Д'.lower()]):
        keys = [*get_predefined_fields('email_address'), 'Пользовательское поле']
        add_new_fields(new_contact, keys)

    handbook.append(new_contact)


def get_path_to_dump(dump_directory: str = 'dumps', file_name: str = 'phonebook', file_extension: str = 'txt') -> str:
    full_file_name = f'{file_name}.{file_extension}'
    
    if dump_directory not in os.listdir():
        os.mkdir(dump_directory)

    if full_file_name not in os.listdir(temp := f'{os.curdir}{os.sep}{dump_directory}'):
        with open(f'{temp}{os.sep}{full_file_name}', 'w', encoding=ENCODING):
            pass

    return os.path.join(f'{os.path.dirname(__file__)}{os.sep}{dump_directory}{os.sep}{full_file_name}')


def make_dump(handbook: list, path: str) -> None:

    with open(path,  'w', encoding=ENCODING) as file:
        json.dump(handbook, file, ensure_ascii=False)


def get_dump(path: str) -> list:
    if os.stat(path).st_size:
        with open(path, 'r', encoding=ENCODING) as file:
            dump = json.load(file)
    else:
        dump = list()
    return dump


def get_commands() -> dict:
    return {
            'Создать': create,
            'Найти': find,
            'Показать': read,
            'Изменить': update,
            'Удалить': delete,
            'Завершить': 0
            }


def menu(handbook: list) -> int:
    commands = get_commands()
    numerated_list = list(enumerate(commands, 1))
    print('Выберите команду по номеру:',
          '\n'.join(f'{num}. {key}' for num, key in numerated_list), sep='\n')

    while choice := input('>>> '):
        try:
            command_index = int(choice) - 1
            if command_index < 0 or len(commands) - 1 < command_index:
                raise IndexError
        except ValueError:
            print(f'Ошибка ввода, не удалось преобразовать {choice} к индексу команды. Повторите ввод.')
            continue
        except IndexError:
            print('Такой команды пока нет, повторите ввод.')
            continue
        except Exception as ex:
            print(f'Введено "{choice}":', ex)
            continue
        else:
            if func := commands[numerated_list[command_index][1]]:
                if value := func(handbook):
                    print(value if isinstance(value, str) else read(value))
                return 1
            return 0


def main() -> None:
    path_to_dump = get_path_to_dump()
    handbook = get_dump(path_to_dump)
    while menu(handbook):
        pass
    handbook.sort(key=lambda el: f'{el["Фамилия"]} {el["Имя"]}')
    make_dump(handbook, path_to_dump)


if __name__ == '__main__':
    main()