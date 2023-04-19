# Класс  Корабль
class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._cells = [1 for x in range(length)]
        self._is_move = True

    # установка начальных координат
    def set_start_coords(self, x, y):                   
        self._x, self._y = x, y

    # получение начальных координат корабля в виде кортежа x, y
    def get_start_coords(self):                         
        return tuple(self._x, self._y)

    # перемещение корабля в направлении его ориентации на go клеток
    def move(self, go):
        if self._is_move == True:
            pass

    # проверка на столкновение с другим кораблем ship
    def is_collide(self, ship):
        pass

    # проверка на выход корабля за пределы игрового поля
    def is_out_pole(self, size):
        pass

    # считывание значения из _cells по индексу indx
    def __getitem__(self, item):
        if 0 <= item <= len(self._cells):
            return self._cells[item]

    # запись нового значения в коллекцию _cells
    def __setitem__(self, key, value):
        self._cells[key] = value