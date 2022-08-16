import typing


class RingDeque(typing.MutableSequence):

    def __init__(self, iterable=None, *, maxlen):
        if maxlen < 0:
            raise ValueError('maxlen must be positive')
        self.maxlen = maxlen
        self._buffer = [None for _ in range(maxlen)]
        self._start_index = 0
        self._items_amount = 0
        if iterable:
            self.extend(iterable)

    def __getitem__(self, index):
        if not -len(self) <= index <= len(self) - 1:
            raise IndexError('deque index out of range')
        # Выбираем правильный положительный индекс в зависимости
        # от знака переданного индекса.
        index = index if index >= 0 else len(self) + index
        return self._buffer[(self._start_index + index) % self.maxlen]

    def __setitem__(self, index, value):
        if not -len(self) <= index <= len(self) - 1:
            raise IndexError('deque index out of range')
        # Выбираем правильный положительный индекс в зависимости
        # от знака переданного индекса.
        index = index if index >= 0 else len(self) + index
        self._buffer[(self._start_index + index) % self.maxlen] = value

    def __delitem__(self, index):
        if not -len(self) <= index <= len(self) - 1:
            raise IndexError('deque index out of range')
        # Выбираем правильный положительный индекс в зависимости
        # от знака переданного индекса.
        index = index if index >= 0 else len(self) + index
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
            self._start_index = (self._start_index + 1) % self.maxlen
        self._items_amount -= 1

    def __len__(self):
        return self._items_amount

    def __eq__(self, other):
        return isinstance(other, RingDeque) and list(self) == list(other)

    def __add__(self, other):
        if not isinstance(other, RingDeque):
            cls = type(other)
            raise TypeError(f'can only concatinate RingDeque (not {cls.__name__}) to RingDeque')
        return RingDeque(list(self) + list(other), maxlen=self.maxlen)

    def __iadd__(self, other):
        self.extend(list(other))
        return self

    def __mul__(self, n):
        multiplied_deque = RingDeque([], maxlen=self.maxlen)
        if n <= 0:
            return multiplied_deque
        for _ in range(n):
            multiplied_deque.extend(list(self))
        return multiplied_deque

    def __imul__(self, n):
        if n <= 0:
            return RingDeque([], maxlen=self.maxlen)
        for _ in range(n - 1):
            self.extend(list(self))
        return self

    def __rmul__(self, n):
        return self * n

    def __copy__(self):
        return RingDeque(list(self), maxlen=self.maxlen)

    def __repr__(self):
        items = [item for item in self]
        return f'RingDeque({items}, maxlen={self.maxlen})'

    def append(self, item):
        # В случае нулевой длины очереди, никакие элементы не могут
        # быть добавлены.
        if self.maxlen == 0:
            return
        if len(self) < self.maxlen:
            self._items_amount += 1
            self[-1] = item
        else:
            self[0] = item
            self._start_index = (self._start_index + 1) % self.maxlen

    def appendleft(self, item):
        # В случае нулевой длины очереди, никакие элементы не могут
        # быть добавлены.
        if self.maxlen == 0:
            return
        if len(self) < self.maxlen:
            self._items_amount += 1
        self._start_index = (self._start_index - 1) % self.maxlen
        self[0] = item

    def extendleft(self, iterable):
        for i in iterable:
            self.appendleft(i)

    def copy(self):
        return self.__copy__()

    def insert(self, index, item):
        if len(self) == self.maxlen:
            raise IndexError('deque already at its maximum size')
        # Если модуль индекса больше, чем количество элементов в очереди,
        # item должен попасть в начало или в конец очереди в зависимости
        # от того, положительный или отрицательный индекс был передан.
        if abs(index) >= len(self):
            index = len(self) if index > 0 else 0
        else:
            # Выбираем правильный положительный индекс в зависимости
            # от знака переданного индекса.
            index = index if index >= 0 else len(self) + index
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
        # В случае нулевой длины очереди, вращать ее не получится.
        if self.maxlen == 0:
            return
        # Нормализуем n для случаев, когда abs(n) > len(self).
        n = n % len(self)
        # При полностью заполненом буфере достаточно изменить
        # позицию старта в буфере.
        if len(self) == self.maxlen:
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
