from random import randint, shuffle
from typing import Union


class Ship:
    """Класс для представления кораблей"""

    HORIZONTAL = 1
    VERTICAL = 2

    def __init__(self, length: int, tp: int = HORIZONTAL, x: int = None, y: int = None):
        self._length = length  # длина корабля
        self._tp = tp  # ориентация корабля(1 - горизонтальная, 2 - вертикальная)
        self._x = x  # координаты начала корабля(первая палуба)
        self._y = y
        self._is_move = True  # возможность перемещения корабля(если не было попадания - True, иначе False)
        self._cells = [1] * length  # список с палубами корабля(1 - попадания не было, 2 - попадание было)

    def __repr__(self):
        return f'({self._length}-палубный, {"Горизонтальный" if self._tp == 1 else "Вертикальный"}, ' \
               f'{"Целый" if self._is_move else "Подбитый"}, ' \
               f'x={self._x} y={self._y})'

    def __setattr__(self, key, value):
        if key in ('_x', '_y', '_length'):
            if not isinstance(value, int) and value is not None or \
                    isinstance(value, int) and value < 0:
                raise TypeError('Координаты и длина должны быть целыми положительными числами')

        if key == '_tp':
            if not isinstance(value, int) or value not in (1, 2):
                raise ValueError('Значение ориентации должно быть 1 или 2')

        super().__setattr__(key, value)

    def __bool__(self):
        """Метод для проверки состояния корабля
        False - если корабль полностью уничтожен,
        True - если есть еще целые палубы"""
        return not all(x == 2 for x in self._cells)

    @property
    def tp(self):
        return self._tp

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def length(self):
        return self._length

    @property
    def is_move(self):
        return self._is_move

    @is_move.setter
    def is_move(self, value):
        if type(value) == bool:
            self._is_move = value

    def set_start_coords(self, x: int, y: int):
        """Метод для установки начальных координат корабля"""
        self._x = x
        self._y = y

    def get_start_coords(self) -> tuple:
        """Получение начальных координат корабля"""
        return self._x, self._y

    def move(self, go: int):
        """Метод реализует перемещения корабля в направлении его ориентации на 'go' клеток"""
        if self._is_move:
            x, y = self.get_start_coords()
            if self._tp == self.HORIZONTAL:
                self.set_start_coords(x + go, y)
            elif self._tp == self.VERTICAL:
                self.set_start_coords(x, y + go)

    @staticmethod
    def _get_place_and_around_coordinates(ship_orientation: int, ship: 'Ship') -> tuple:
        """Метод для получения координат нахождения всего корабля и
        координат вокруг корабля"""
        indexes = (-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)  # индексы вокруг клетки
        all_coord = set()  # координаты корабля и координаты вокруг корабля
        ship_coord = set()  # координаты только корабля
        x, y, length = ship._x, ship._y, ship._length

        if ship_orientation == ship.HORIZONTAL:
            ship_coord = {(x + j, y) for j in range(length)}  # сбор координат каждой палубы корабля

        elif ship_orientation == ship.VERTICAL:
            ship_coord = {(x, y + i) for i in range(length)}

        # сбор координат вокруг корабля и самого корабля
        for a, b in indexes:
            for c, d in ship_coord:
                all_coord.add((a + c, b + d))

        return all_coord, ship_coord

    def is_collide(self, ship: 'Ship') -> bool:
        """Метод для проверки на столкновение или соприкосновение с другим кораблем 'ship'"""
        if isinstance(ship, Ship):
            # получение координат текущего корабля и другого корабля
            all_coord_self, self_coord = self._get_place_and_around_coordinates(self._tp, self)
            all_coord_ship, ship_coord = ship._get_place_and_around_coordinates(ship._tp, ship)
            common_coord = all_coord_self & all_coord_ship  # общие координаты двух кораблей
            # координаты мест пересечения кораблей(если таких нет - значит корабли не пересекаются и не касаются)
            result = (self_coord & common_coord) | (ship_coord & common_coord)
            return len(result) != 0

    def is_out_pole(self, size: int) -> bool:
        """Метод для проверки на выход корабля за пределы игрового поля"""
        x, y = self._x, self._y
        last_part_coord = (x + self._length - 1, y) if self._tp == self.HORIZONTAL else (x, y + self._length - 1)
        return x < 0 or last_part_coord[0] > size - 1 or y < 0 or last_part_coord[1] > size - 1

    def _check_index(self, index) -> bool:
        """Метод для проверки индекса для работы со списком _cells"""
        return 0 <= index < len(self._cells)

    def __getitem__(self, item: int) -> int:
        """Метод для считывания значения из списка _cells по индексу item"""
        if self._check_index(item):
            return self._cells[item]

    def __setitem__(self, key, value):
        """Метод для записи нового значения в _cells по индексу key"""
        if self._check_index(key) and isinstance(value, int) and value in (1, 2):
            self._cells[key] = value


class GamePole:
    """Класс для описания игрового поля"""

    def __init__(self, size: int = 10):
        self._size = size  # размер игрового поля
        self._ships = []  # список из кораблей на поле
        self._field = [[0] * self._size for _ in range(self._size)]  # игровое поле
        self._name = ''
        self._count_dead_ships = 0
        self._generate_ships()  # создание кораблей

    def __bool__(self):
        return self._count_dead_ships == 10

    @property
    def ships(self):
        return self._ships

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value

    @property
    def count_dead_ships(self):
        return self._count_dead_ships

    @count_dead_ships.setter
    def count_dead_ships(self, value):
        if isinstance(value, int):
            self._count_dead_ships = value

    def _check_ships_around(self, length: int, head_coord: tuple, orientation: int) -> int:
        """Метод для проверки наличия кораблей вокруг и на месте установки корабля"""
        indexes = (-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)
        head_x, head_y = head_coord
        result = 0

        if orientation == 1:  # горизонтально
            j = head_x
            k = 0
            while length > k:  # пока не проверили на наличие кораблей вокруг и на месте установки
                result += sum(self._field[head_y + x][j + y] for x, y in indexes
                              if 0 <= head_y + x < self._size and 0 <= j + y < self._size)
                j += 1
                k += 1

        elif orientation == 2:  # вертикально
            i = head_y
            k = 0
            while length > k:  # пока не проверили на наличие кораблей вокруг и на месте установки
                result += sum(self._field[i + x][head_x + y] for x, y in indexes
                              if 0 <= i + x < self._size and 0 <= head_x + y < self._size)
                i += 1
                k += 1

        return result

    def _generate_ships(self):
        """Метод для создания кораблей со случайной ориентацией и без начальных координат"""
        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))]

    def init(self):
        """Метод для начальной инициализации игрового поля"""
        for ship in self._ships:
            tp, length = ship.tp, ship.length
            while True:  # пока корабли не расставлены
                x, y = randint(0, self._size - 1), randint(0, self._size - 1)  # ship_x -> j; ship_y -> i
                if tp == ship.HORIZONTAL:  # если расположение корабля горизонтальное
                    if x + (length - 1) > self._size - 1:  # если длина корабля выходит за поле
                        continue

                    result = self._check_ships_around(length, (x, y), tp)

                    if not result:  # если кораблей нет рядом и нет на месте
                        k = 0
                        for j in range(x, x + length):
                            self._field[y][j] = ship[k]  # установка корабля на поле с k-палубами
                            k += 1
                    else:
                        continue

                elif tp == ship.VERTICAL:  # если расположение корабля вертикальное
                    if y + (length - 1) > self._size - 1:  # если длина корабля выходит за поле
                        continue

                    result = self._check_ships_around(length, (x, y), tp)

                    if not result:  # если кораблей нет рядом и нет на месте
                        k = 0
                        for i in range(y, y + length):
                            self._field[i][x] = ship[k]
                            k += 1
                    else:
                        continue

                ship.set_start_coords(x, y)  # установить в текущем корабле его начальные координаты
                break

    def get_ships(self) -> list:
        """Метод для возврата списка кораблей на поле"""
        return self._ships

    def update_game_field(self):
        """Метод для обновления игрового поля
        после движения кораблей и после каждого хода"""
        for i in range(self._size):  # обнуление поля
            for j in range(self._size):
                self._field[i][j] = 0

        for ship in self._ships:
            x, y, length = ship.x, ship.y, ship.length
            ship_part = 0

            if ship.tp == ship.HORIZONTAL:
                for j in range(x, x + length):
                    self._field[y][j] = ship[ship_part]  # установка корабля на поле с k-палубами
                    ship_part += 1
            elif ship.tp == ship.VERTICAL:
                for i in range(y, y + length):
                    self._field[i][x] = ship[ship_part]
                    ship_part += 1

    def move_ships(self):
        """Метод для перемещения каждого корабля на одну клетку"""
        for ship in self._ships:
            old_x, old_y = ship.get_start_coords()
            directions = ['forward', 'back']  # допустимые направления движения
            is_conflict = False
            while directions or not is_conflict:
                shuffle(directions)  # перемешивание списка с направлениями
                direction = directions.pop()  # и взятие первого

                x = y = 0  # переменные для новых (возможных) координат
                if direction == 'forward' and ship.tp == ship.HORIZONTAL and ship.is_move:
                    x = ship.x + 1
                    y = ship.y
                elif direction == 'back' and ship.tp == ship.HORIZONTAL and ship.is_move:
                    x = ship.x - 1
                    y = ship.y
                elif direction == 'forward' and ship.tp == ship.VERTICAL and ship.is_move:
                    x = ship.x
                    y = ship.y + 1
                elif direction == 'back' and ship.tp == ship.VERTICAL and ship.is_move:
                    x = ship.x
                    y = ship.y - 1
                else:
                    break

                try:
                    ship.set_start_coords(x, y)  # пробуем применить новые координаты начала для корабля
                except TypeError:  # если координаты меньше 0, то ловим исключение и пробуем другое направление
                    continue

                if ship.is_out_pole(self._size):  # если корабль выходит за поле - попробовать другое направление
                    ship.set_start_coords(old_x, old_y)
                    continue

                for curr_ship in self._ships:
                    if curr_ship != ship:
                        if not ship.is_collide(curr_ship):  # проверка столкновения текущего корабля с другими
                            continue
                        else:  # если было столкновение или пересечение
                            ship.set_start_coords(old_x, old_y)  # сброс новых координат до начальных
                            is_conflict = True  # и установка флага конфликта
                            break
                if is_conflict:  # если был обнаружен конфликт - попробовать переместить корабль в другую сторону
                    continue
                break

        self.update_game_field()  # обновить поле с новым размещением кораблей

    def show(self):
        """Метод для отображения игрового поля в консоли"""
        print(f'{self.name:^{self._size * 2}}')
        print(' '.join(chr(i) for i in range(97, 97 + self._size)))
        print('-' * (self._size * 2 - 1))

        for i, row in enumerate(self._field, 1):
            print(f'{" ".join(str(s) for s in row)}  {i}')
        print('_' * (self._size * 2 - 1))
        print()

    def get_pole(self) -> tuple:
        """Метод для получения текущего игрового поля"""
        return tuple(tuple(row) for row in self._field)

    def __repr__(self) -> str:
        return f'Размер поля - {self._size} x {self._size}'


class SeaBattle:
    """Класс для настройки и работы игрового процесса"""
    _x_coord_translate = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10}
    _comp_ships_coord = {}  # координаты всех палуб кораблей компьютера
    _human_ships_coord = {}  # координаты всех палуб кораблей человека

    def __init__(self, size_field, name_1: str = 'Computer', name_2: str = 'Human'):
        self._size_field = size_field
        self.computer, self.human = GamePole(size_field), GamePole(size_field)
        self.computer.name, self.human.name = name_1, name_2  # имена игроков
        self._hit_points_comp = []  # координаты, в которые уже был выстрел
        self._hit_points_human = []
        self.result_field = [['-'] * self._size_field for _ in range(self._size_field)]

    def init(self):
        """Метод инициализации полей компьютера и человека.
        Метод производит расстановку кораблей на полях соперников"""
        self.computer.init()
        self.human.init()
        self._comp_ships_coord = self.get_all_ships_parts_coord(self.computer)
        self._human_ships_coord = self.get_all_ships_parts_coord(self.human)

    @staticmethod
    def get_all_ships_parts_coord(field: GamePole) -> dict:
        """Метод для получения координат всех палуб кораблей"""
        ships = field.ships  # получение списка всех кораблей поля
        ship_coord = {ship: [] for ship in ships}  # словарь с будущими координатами палуб
        for ship, coord in ship_coord.items():
            x, y = ship.get_start_coords()
            length = ship.length
            for i in range(length):
                next_x_y = (x + i, y) if ship.tp == ship.HORIZONTAL else (x, y + i)
                coord.append(next_x_y)

        return ship_coord

    def recognize_shell_place(self, shell_coord: tuple, gamer: GamePole) -> Union[Ship, None]:
        """Метод для распознавания места попадания снаряда"""
        ships = self._comp_ships_coord if gamer is self.human else self._human_ships_coord
        place = list(filter(lambda x: shell_coord in ships[x], ships))
        return place[0] if place else None  # если есть попадание в корабль - вернуть корабль

    def human_go(self):
        """Метод для реализации хода человека"""
        x = y = None
        while True:
            try:
                coord = input('Введите координаты поля для выстрела в формате \'a1\': ')
                x, y = coord[0], str(coord[1:])
            except (TypeError, IndexError, ValueError):
                print('Введен не верный тип и/или диапазон координат')
                continue
            else:
                if coord[0].lower() in [chr(let) for let in range(97, 97 + self._size_field)] and \
                        coord[1] in [str(d) for d in range(1, self._size_field + 1)]:
                    x, y = self._x_coord_translate.get(x) - 1, int(y) - 1
                    if (x, y) in self._hit_points_human:
                        print('Координаты уже использовались')
                        continue
                    break
                continue

        shell_place = self.recognize_shell_place((x, y), self.human)  # определение места попадания снаряда
        self._hit_points_human.append((x, y))  # и сохранение координат места в список

        if shell_place is not None:  # если есть попадание в корабль
            self._marked_broken_ship_part(self.human, shell_place, (x, y))
            self.computer.update_game_field()  # обновление поля и его отображение
            self.show_shot_location(x, y, 'X')  # отобразить на другом поле попадание по кораблю на x, y координате
        else:
            self.show_shot_location(x, y, '*')  # отобразить на другом поле промах на x, y координате

    def _marked_broken_ship_part(self, gamer: GamePole, shell_place: Ship, coord_place: tuple):
        """Метод реализует поиск подбитой палубы корабля и отмечает ее как уничтоженную"""
        ships_coord = self._human_ships_coord if gamer is self.computer else self._comp_ships_coord
        part_num = ships_coord.get(shell_place).index(coord_place)  # получаем номер палубы
        shell_place[part_num] = 2  # и помечаем ее 'подбитой'
        shell_place.is_move = False
        if not shell_place:  # если корабль полностью уничтожен - увеличить счетчик уничтоженных кораблей
            gamer.count_dead_ships += 1

    def computer_go(self):
        """Метод для реализации хода компьютера
         случайным образом в свободные клетки"""
        while True:
            x, y = randint(0, self._size_field - 1), randint(0, self._size_field - 1)
            if (x, y) in self._hit_points_comp:
                continue
            break

        shell_place = self.recognize_shell_place((x, y), self.computer)  # определение места попадания снаряда
        self._hit_points_comp.append((x, y))  # и сохранение координат места в список

        if shell_place is not None:  # если есть попадание в корабль
            self._marked_broken_ship_part(self.computer, shell_place, (x, y))
            self.human.update_game_field()  # обновление поля и его отображение
        self.human.show()

    def show_shot_location(self, x: int, y: int, state: str):
        """Метод отображает поле с местом попадания снаряда после выстрела
        Поле отображается только после хода человека; X - было попадание в корабль;
        * - выстрел мимо"""
        self.result_field[y][x] = state

        print(' '.join(chr(i) for i in range(97, 97 + self._size_field)))
        print('-' * (self._size_field * 2 - 1))

        for i, row in enumerate(self.result_field, 1):
            print(f'{" ".join(str(s) for s in row)}  {i}')
        print('_' * (self._size_field * 2 - 1))
        print()

    def __bool__(self):
        """Метод определяет окончание битвы.
        Если кто-то уничтожил все 10 кораблей - игра останавливается"""
        return not self.human and not self.computer