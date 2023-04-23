from random import randint
# Класс  Корабль
class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y 
        self._cells = [1 for x in range(length)]
        self._is_move = True

    # координаты палуб корабля
    def get_coords(self):
        if self._x is None:
            return (None, None),

        width = self._length if self._tp == 1 else 1
        height = self._length if self._tp == 2 else 1
        decks = tuple((x, y) for x in range(self._x, self._x+width) for y in range(self._y, self._y+height))
        return decks

    # установка начальных координат
    def set_start_coords(self, x, y):                   
        self._x, self._y = x, y

    # получение начальных координат корабля в виде кортежа x, y
    def get_start_coords(self):                         
        return tuple(self._x, self._y)

    # перемещение корабля в направлении его ориентации на go клеток
    def move(self, go):
        if self._is_move == True:
            if self._tp == 1:
                self._x += go
            else:
                self._y += go

    # проверка на столкновение с другим кораблем ship
    def is_collide(self, ship):
        ship_decks = set(ship.get_coords())
        return bool(self.area & ship_decks)

    # область вокруг корабля
    @property
    def area(self):
        width = self._length if self._tp == 1 else 1
        height = self._length if self._tp == 2 else 1
        around_area = {(x, y) for x in range(self._x-1, self._x+width+1) for y in range(self._y-1, self._y+height+1)}
        return around_area
    

    # проверка на выход корабля за пределы игрового поля
    def is_out_pole(self, size):
        if self._x + self._length <= size-1:
            return True
        if self._y + self._length <= size-1:
            return True

    # считывание значения из _cells по индексу indx
    def __getitem__(self, item):
        if 0 <= item <= len(self._cells):
            return self._cells[item]

    # запись нового значения в коллекцию _cells
    def __setitem__(self, key, value):
        self._cells[key] = value


# Класс игрового поля
class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []

    # начальная инициализация игрового поля
    def init(self):
        self._ships = [Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), 
                       Ship(4, tp=randint(1, 2))
                      ]

    # возвращает коллекцию _ships  
    def get_ships(self):
        pass

    # перемещает каждый корабль из коллекции _ships на одну клетку
    def move_ships(self):
        pass

    # отображение игрового поля в консоли
    def show(self):
        pass

    #  получение текущего игрового поля
    def get_pole(self):
        pass