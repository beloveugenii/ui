# libsui.py

from os import popen
from time import sleep
from json import load

version = '0.0.2.7'

def helps(text, delay=0):
    # Принимает два параметра: строку для вывода и задержку времени показа сообщения в секундах
    print(text)
    sleep(delay) if delay != 0 else input()
    return False

def get_terminal_width():
    rows, columns = popen('stty size', 'r').read().split()
    rows, columns = int(rows), int(columns)
    return columns

def get_dict_from_json(file, key):
    # Функция принимает имя json-файла и ключ, который нужно экспориторовать
    # Возвращает ассоциативный массив из данных по переданному ключу
    with open(file) as f:
        templates = load(f)
    return dict(tuple(templates[key]))

def get_list_from_json(file, key):
    # Функция принимает имя json-файла и ключ, который нужно экспориторовать
    # Возвращает список из данных по переданному ключу
    with open(file) as f:
        templates = load(f)
    return tuple(templates[key])

def line(): print('-' * get_terminal_width())

def clear(): print('\033[H\033[2J', end='')

def hide_cursor(): print("\033[?25l")

def restore_cursor(): print("\033[?25h")

def save_cursor_pos(): print("\033[s")

def restore_cursor_pos(): print("\033[u")

def get_fields_len(array):
    # takes a list of tuples
    fields = []

    # defines the number of rows and columns
    rows = len(array)
    try:
        cols =  max([len(col) for col in array])
    except ValueError:
        cols = 0
    
    # expands each row to the maximum number of columns
    for r in range(rows):
        while len(array[r]) < cols:
                array[r] = array[r] + ('',)
    
    # defines width of every columns
    for c in range(cols):
        fields.append(max(len(str(array[r][c])) for r in range(rows)))
    
    screen_width = get_terminal_width()

    # defines wifth of empty fields 
    sep_len = (screen_width - sum(fields)) // ( len(fields) + 1)
    
    while sum(fields) + (cols + 1) * sep_len > screen_width:
        sep_len -= 1

    # returns list of every columns width and empty field width
    return fields, sep_len


def print_as_table(items, sep=' '):
    # takes the list of tuples
    fields, sep_len = get_fields_len(items)

    # prints tuples elements in fieldd separating with empty spaces
    for row in items:
        for c in range(len(row)):
            print('%s%-*s' % (sep * sep_len, fields[c], row[c]), end='')
        else:
            print('%s' % (sep * sep_len,))

def header(text):
    # takes a string and transform it to list of tuples with single element
    # print a string in center of screen
    line()
    print_as_table([(text,), ])
    line()

def menu(array, cols):
    # takes a list ol menu elements and columns number
    menu_lst = []
    array = list(map(lambda word: '[' + word[0]+ ']' + word[1:], array))

    if len(array) % 2 == 1 and cols % 2 == 0:
        array.append('')
    # convert list to list of tuples
    while len(array) > 0:
        tmp = []
        for t in range(cols):
            try:
                tmp.append(array.pop(0))
            except:
                pass
        menu_lst.append(tuple(tmp))

    # print list of tuples like menu
    line()
    if cols > 0:
        print_as_table(menu_lst)
        line()

def screen(header_title, func, menu_lst, menu_cols, promt='>> '):
    # takes a list with header text, some function, menu list and number of menu columns
    # clear the screen and prints header, output of body function and menu
    clear()
    header(header_title)
    func()
    menu(menu_lst, menu_cols)
    return input(promt).lower().strip()

class Completer():
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # Если какой-то текст передан в метод
            if text:
                # вернуть список слов из списка, которые начинаются на текст
                self.matches = [s for s in self.options if s and s.startswith(text.lstrip())]
            else:
                # иначе вернуть весь список
                self.matches = self.options[:]

        # Вернуть элемент состояния из списка совпадений, если их много. 

        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


