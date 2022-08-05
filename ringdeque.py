import typing


class RingDeque(typing.MutableSequence):

    def __init__(self, iterable=None, *, maxlen):
        if maxlen < 0:
            raise ValueError('maxlen must be positive')
        self._buffer = [None for _ in range(maxlen)]
        self._start_index = 0
        self._items_amount = 0
        if iterable:
            self.extend(iterable)

    def __getitem__(self, index):
        if (index < 0 and abs(index) > self._items_amount or
                index >= self._items_amount):
            raise IndexError('deque index out of range')
        index = index % self._items_amount
        return self._buffer[(self._start_index + index) % len(self._buffer)]

    def __setitem__(self, index, value):
        if (index < 0 and abs(index) > self._items_amount or
                index >= self._items_amount):
            raise IndexError('deque index out of range')
        index = index % self._items_amount
        self._buffer[(self._start_index + index) % len(self._buffer)] = value

    def __delitem__(self, index):
        if (index < 0 and abs(index) > self._items_amount or
                index >= self._items_amount):
            raise IndexError('deque index out of range')
        index = index % len(self)
        # Для удаления нужного элемента, переставляем все стоящие от него
        # справа или слева элементы на 1 ячейку. Направление перестановки
        # выбирается в зависимости от того, в какой половине находится
        # удаляемый элемент. В ячейку, из которой был взят последний
        # переставленный элемент, записываем None для предотвращения
        # утечки памяти.
        if index > len(self) // 2:
            for i in range(index, len(self) - 1):
                self[i] = self[i + 1]
            self[-1] = None
        else:
            for i in reversed(range(1, index + 1)):
                self[i] = self[i - 1]
            self[0] = None
            self._start_index = (self._start_index + 1) % len(self._buffer)
        self._items_amount -= 1

    def __len__(self):
        return self._items_amount

    def __repr__(self):
        items = [item for item in self]
        return f'RingDeque({items}, maxlen={len(self._buffer)})'

    def append(self, item):
        if self._items_amount < len(self._buffer):
            self._items_amount += 1
            self[self._items_amount - 1] = item
        else:
            self[0] = item
            self._start_index = (self._start_index + 1) % len(self._buffer)

    def appendleft(self, item):
        if self._items_amount < len(self._buffer):
            self._items_amount += 1
        self._start_index = (self._start_index - 1) % len(self._buffer)
        self[0] = item

    def extendleft(self, iterable):
        for i in iterable:
            self.appendleft(i)

    def copy(self):
        return RingDeque(list(self), maxlen=len(self._buffer))

    def insert(self, index, item):
        if self._items_amount == len(self._buffer):
            raise IndexError('deque already at its maximum size')
        # Если модуль индекса больше, чем количество элементов в очереди,
        # item должен попасть в начало или в конец очереди в зависимости
        # от того, положительный или отрицательный индекс был передан.
        if abs(index) >= len(self):
            index = len(self) if index > 0 else 0
        # Нормализация индекса на случай его отрицательных значений.
        else:
            index = index % len(self)
        # При вставке в правую часть, все элементы справа смещаются вправо.
        # При вставке в левую часть, все элементы слева смещаются влево.
        # Это сделано для того, чтобы производить меньше смещений элементов в
        # общем случае.
        if index > len(self) // 2:
            self.append(None)
            for i in reversed(range(index + 1, len(self))):
                self[i] = self[i - 1]
        else:
            self.appendleft(None)
            for i in range(0, index + 1):
                self[i] = self[i + 1]
        self[index] = item

    def popleft(self):
        return self.pop(0)

    def rotate(self, n=1):
        # Нормализуем n для случаев.
        n = n % len(self)
        # При полностью заполненом буфере достаточно изменить
        # позицию старта в буфере.
        if len(self) == len(self._buffer):
            self._start_index = (self._start_index - n) % len(self)
        # Для лучшей производительности алгоритма сторона
        # вращения определяется количеством необходимых
        # перестановок.
        elif n <= len(self) // 2:
            for _ in range(n):
                self.appendleft(self.pop())
        else:
            for _ in range(len(self) - n):
                self.append(self.popleft())
