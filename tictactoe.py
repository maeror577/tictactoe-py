"""
Игра «Крестики-нолики».
Итоговое практическое задание B5.6 для SkillFactory.
Поддерживается 3 режима игры: автоматический, с компьютерным оппонентом или
вдвоём. Используются модули только из стандартной библиотеки Python 3.8.5.

TODO: Отображение текущих игроков
"""


import os
import random
import time


def print_intro(playfield):
    """
    Функция очистки экрана консоли (*), вывода заголовка и текущего
    состояния игрового поля.
    Аргументы:
    playfield — текущее состояние игрового поля

    (*) Команда 'cls' для систем на основе Windows NT, команда 'clear' для
    UNIX-подобных систем.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print('-------------------------')
    print('|    Крестики-нолики    |')
    print('|                       |')
    print('|  формат ввода ходов:  |')
    print('|    «строка колонка»   |')
    print('-------------------------')
    print()
    print(' ', *range(1, 4), sep=' ')
    for i in range(1, 4):
        print(str(i), end=' ')
        print(*playfield[i - 1], sep=' ')
    print()


def unwrap_playfield(playfield):
    """
    Функция развёртки игрового поля на списки рядов, колонок и диагоналей.
    Аргументы:
    playfield — текущее состояние игрового поля
    """
    list_of_rows = playfield
    list_of_columns = list(map(list, zip(*playfield)))
    list_of_diagonals = [[list_of_rows[i][i] for i in range(3)],
                        [list_of_rows[::-1][i][i] for i in range(3)]]
    # Наверное, короче было диагонали вручную прописать, но хотелось
    # автоматизации, программирование, всё-таки! А list_of_rows используется
    # просто для наглядности.
    return list_of_rows, list_of_columns, list_of_diagonals


def human_player_move(playfield):
    """
    Ход человеческого игрока.
    Аргументы:
    playfield — текущее состояние игрового поля
    """
    while True:
        try:
            row, col = map(int, input().split())
            if playfield[row - 1][col - 1] != '-':
                print_intro(playfield)
                print(f'Клетка {row}-{col} занята!')
                continue
        except (IndexError, ValueError):
            print_intro(playfield)
            print('Введите корректные значения!')
            continue
        else:
            # Возвращаем координаты с учётом того, что индексы матрицы
            # на 1 меньше координат, указанных на экране
            return row - 1, col - 1


def computer_player_move(playfield, player_symbol):
    """
    Ход компьютерного игрока.
    Аргументы:
    playfield — текущее состояние игрового поля
    player_symbol — знак игрока
    """
    rows, cols, diags = unwrap_playfield(playfield)
    opposite_player_symbol = 'O' if player_symbol == 'X' else 'X'

    # В первую очередь компьютер пытается выиграть, проверяя ряды, затем
    # колонки, а затем каждую из диагоналей на наличие двух своих символов.
    for row_number, row in enumerate(rows):
        if row.count(player_symbol) == 2 and row.count('-') == 1:
            return row_number, row.index('-')
    for col_number, col in enumerate(cols):
        if col.count(player_symbol) == 2 and col.count('-') == 1:
            return col.index('-'), col_number
    if diags[0].count(player_symbol) == 2 and diags[0].count('-') == 1:
        return diags[0].index('-'), diags[0].index('-')
    if diags[1].count(player_symbol) == 2 and diags[1].count('-') == 1:
        return 2 - diags[1].index('-'), diags[1].index('-')

    # Затем компьютер пытается не проиграть, действуя точно так же.
    for row_number, row in enumerate(rows):
        if row.count(opposite_player_symbol) == 2 and row.count('-') == 1:
            return row_number, row.index('-')
    for col_number, col in enumerate(cols):
        if col.count(opposite_player_symbol) == 2 and col.count('-') == 1:
            return col.index('-'), col_number
    if diags[0].count(opposite_player_symbol) == 2 and diags[0].count('-') == 1:
        return diags[0].index('-'), diags[0].index('-')
    if diags[1].count(opposite_player_symbol) == 2 and diags[1].count('-') == 1:
        return 2 - diags[1].index('-'), diags[1].index('-')

    # Наконец, если ни то, ни другое ему не грозит, то компьютер
    # просто ходит случайным образом.
    while True:
        row_number = random.randrange(3)
        col_number = random.randrange(3)
        if playfield[row_number][col_number] == '-':
            return row_number, col_number

    # В итоге, компьютерный оппонент достаточно глупый, и скорее создаёт
    # видимость игры, но хотя бы мешает побеждать.


def is_it_win(playfield, player_symbol):
    """
    Проверка условий победы.
    Аргументы:
    playfield — текущее состояние игрового поля
    player_symbol — знак игрока
    """
    rows, cols, diags = unwrap_playfield(playfield)
    list_all = rows + cols + diags

    for case in list_all:
        if set(case) == {player_symbol}:
            return True
    return False


def tictactoe():
    """ Основная игровая функция. """
    playfield = [['-' for row in range(3)] for col in range(3)]
    turn_count = 0
    player_symbol = 'X'

    print_intro(playfield)
    player1 = input('Игрок 1: человек (y) или компьютер (n)? ') in ('y', 'Y')
    player2 = input('Игрок 2: человек (y) или компьютер (n)? ') in ('y', 'Y')

    # Максимально возможное количество ходов == 9
    while turn_count < 9:
        turn_count += 1
        current_player = player1 if turn_count % 2 else player2

        print_intro(playfield)
        print(f'Раунд №{turn_count}')
        print(f'Ход {player_symbol}: ', end='', flush=True)
        if current_player:
            row, col = human_player_move(playfield)
        else:
            row, col = computer_player_move(playfield, player_symbol)
            time.sleep(1)
            print(f'{row + 1} {col + 1}')
            time.sleep(1)
            # Выставлены секундные задержки, чтобы было понятно,
            # как сходил компьютер.

        playfield[row][col] = player_symbol
        if is_it_win(playfield, player_symbol):
            print_intro(playfield)
            print(f'Победа {player_symbol}!')
            break

        # Передача хода следующему игроку
        player_symbol = 'O' if player_symbol == 'X' else 'X'

    # Если условие победы не сработало на последнем ходу,
    # значит, игра закончилась ничьей
    if not is_it_win(playfield, player_symbol):
        print_intro(playfield)
        print('Ничья!')

    restart = input('\nХотите сыграть ещё раз? (y/n)\n')
    if restart in ('y', 'Y'):
        tictactoe()

    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    tictactoe()
