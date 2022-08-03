from copy import copy

import pytest

from ringdeque import RingDeque


class TestRingDeque:

    def test_init(self):
        deque = RingDeque(maxlen=3)
        assert list(deque) == []

        deque = RingDeque(iter([1, 2]), maxlen=3)
        assert list(deque) == [1, 2]

        deque = RingDeque(iter([1, 2, 3]), maxlen=3)
        assert list(deque) == [1, 2, 3]

        deque = RingDeque(iter([1, 2, 3, 4]), maxlen=3)
        assert list(deque) == [2, 3, 4]

        with pytest.raises(ValueError):
            RingDeque(maxlen=-5)

    def test_append(self):
        deque = RingDeque([1, 2, 3], maxlen=5)

        deque.appendleft(0)
        assert list(deque) == [0, 1, 2, 3]

        deque.append(4)
        assert list(deque) == [0, 1, 2, 3, 4]

    def test_append_full(self):
        deque = RingDeque([1, 2, 3], maxlen=3)

        deque.append(4)
        assert list(deque) == [2, 3, 4]

        deque = RingDeque([1, 2, 3], maxlen=3)

        deque.appendleft(0)
        assert list(deque) == [0, 1, 2]

    def test_append_sequence(self):
        deque = RingDeque(maxlen=3)

        deque.appendleft(1)
        assert list(deque) == [1]

        deque.append(2)
        assert list(deque) == [1, 2]

        deque.appendleft(3)
        assert list(deque) == [3, 1, 2]

        deque.append(4)
        assert list(deque) == [1, 2, 4]

        deque.append(5)
        assert list(deque) == [2, 4, 5]

        deque.appendleft(6)
        assert list(deque) == [6, 2, 4]

        deque.appendleft(7)
        assert list(deque) == [7, 6, 2]

        deque.append(8)
        assert list(deque) == [6, 2, 8]

        deque.appendleft(9)
        assert list(deque) == [9, 6, 2]

    def test_extend(self):
        deque = RingDeque([1], maxlen=5)

        deque.extendleft([2, 3])
        assert list(deque) == [3, 2, 1]

        deque.extend([4, 5])
        assert list(deque) == [3, 2, 1, 4, 5]

        deque.extendleft([6, 7])
        assert list(deque) == [7, 6, 3, 2, 1]

        deque.extend([8, 9])
        assert list(deque) == [3, 2, 1, 8, 9]

    def test_insert(self):
        deque = RingDeque([1, 2, 3], maxlen=7)
        deque.insert(0, 100)
        assert list(deque) == [100, 1, 2, 3]

        deque = RingDeque([1, 2, 3], maxlen=7)
        deque.insert(1, 100)
        assert list(deque) == [1, 100, 2, 3]

        deque = RingDeque([1, 2, 3], maxlen=7)
        deque.insert(3, 100)
        assert list(deque) == [1, 2, 3, 100]

        deque = RingDeque([1, 2, 3], maxlen=7)
        deque.insert(100, 100)
        assert list(deque) == [1, 2, 3, 100]

        deque = RingDeque([1, 2, 3], maxlen=7)
        deque.insert(-1, 100)
        assert list(deque) == [1, 2, 100, 3]

        deque = RingDeque([1, 2, 3], maxlen=7)
        deque.insert(-3, 100)
        assert list(deque) == [100, 1, 2, 3]

        deque = RingDeque([1, 2, 3], maxlen=7)
        deque.insert(-100, 100)
        assert list(deque) == [100, 1, 2, 3]

    def test_insert_full(self):
        deque = RingDeque([1, 2, 3], maxlen=3)
        with pytest.raises(IndexError):
            deque.insert(0, 4)
        with pytest.raises(IndexError):
            deque.insert(-1, 4)

        deque = RingDeque(maxlen=0)
        with pytest.raises(IndexError):
            deque.insert(0, 1)
        with pytest.raises(IndexError):
            deque.insert(-1, 1)

    def test_get_item(self):
        deque = RingDeque([1, 2, 3], maxlen=5)
        deque.appendleft(0)
        deque.append(4)

        assert deque[0] == 0
        assert deque[1] == 1
        assert deque[4] == 4
        assert deque[-1] == 4
        assert deque[-2] == 3
        assert deque[-5] == 0
        with pytest.raises(IndexError):
            deque[5]  # noqa
        with pytest.raises(IndexError):
            deque[-6]  # noqa

    def test_set_item(self):
        deque = RingDeque([1, 2, 3], maxlen=5)
        deque.appendleft(0)
        deque.append(4)

        deque[0] = 10
        assert list(deque) == [10, 1, 2, 3, 4]

        deque[1] = 11
        assert list(deque) == [10, 11, 2, 3, 4]

        deque[4] = 14
        assert list(deque) == [10, 11, 2, 3, 14]

        deque[-1] = 24
        assert list(deque) == [10, 11, 2, 3, 24]

        deque[-2] = 23
        assert list(deque) == [10, 11, 2, 23, 24]

        deque[-5] = 20
        assert list(deque) == [20, 11, 2, 23, 24]

        with pytest.raises(IndexError):
            deque[5] = 15
        assert list(deque) == [20, 11, 2, 23, 24]

        with pytest.raises(IndexError):
            deque[-6] = 26
        assert list(deque) == [20, 11, 2, 23, 24]

    def test_del_item(self):
        deque = RingDeque([3, 4, 5, 6, 7, 8], maxlen=10)
        deque.extendleft([2, 1, 0])

        del deque[7]
        assert list(deque) == [0, 1, 2, 3, 4, 5, 6, 8]

        del deque[7]
        assert list(deque) == [0, 1, 2, 3, 4, 5, 6]

        del deque[0]
        assert list(deque) == [1, 2, 3, 4, 5, 6]

        del deque[3]
        assert list(deque) == [1, 2, 3, 5, 6]

        del deque[-1]
        assert list(deque) == [1, 2, 3, 5]

        del deque[-4]
        assert list(deque) == [2, 3, 5]

        del deque[-2]
        assert list(deque) == [2, 5]

        with pytest.raises(IndexError):
            del deque[2]
        assert list(deque) == [2, 5]

        with pytest.raises(IndexError):
            del deque[-3]
        assert list(deque) == [2, 5]

    def test_pop(self):
        deque = RingDeque([3, 4, 5, 6, 7], maxlen=10)
        deque.extendleft([2, 1, 0])

        deque.pop()
        assert list(deque) == [0, 1, 2, 3, 4, 5, 6]

        deque.pop()
        assert list(deque) == [0, 1, 2, 3, 4, 5]

        deque.popleft()
        assert list(deque) == [1, 2, 3, 4, 5]

        deque.popleft()
        assert list(deque) == [2, 3, 4, 5]

        deque.pop()
        assert list(deque) == [2, 3, 4]

        deque.pop(0)
        assert list(deque) == [3, 4]

        deque.pop(1)
        assert list(deque) == [3]

        with pytest.raises(IndexError):
            deque.pop(5)
        assert list(deque) == [3]

        with pytest.raises(IndexError):
            deque.pop(-5)
        assert list(deque) == [3]

        deque.popleft()
        assert list(deque) == []

        with pytest.raises(IndexError):
            deque.pop()
        assert list(deque) == []

        with pytest.raises(IndexError):
            deque.popleft()
        assert list(deque) == []

    def test_rotate(self):
        deque = RingDeque([3, 4, 5], maxlen=10)
        deque.extendleft([2, 1, 0])

        deque.rotate(0)
        assert list(deque) == [0, 1, 2, 3, 4, 5]

        deque.rotate(1)
        assert list(deque) == [5, 0, 1, 2, 3, 4]

        deque.rotate(2)
        assert list(deque) == [3, 4, 5, 0, 1, 2]

        deque.rotate(6)
        assert list(deque) == [3, 4, 5, 0, 1, 2]

        deque.rotate(13)
        assert list(deque) == [2, 3, 4, 5, 0, 1]

        deque.rotate(-1)
        assert list(deque) == [3, 4, 5, 0, 1, 2]

        deque.rotate(-3)
        assert list(deque) == [0, 1, 2, 3, 4, 5]

        deque.rotate(-6)
        assert list(deque) == [0, 1, 2, 3, 4, 5]

        deque.rotate(-13)
        assert list(deque) == [1, 2, 3, 4, 5, 0]

    def test_rotate_full(self):
        deque = RingDeque([3, 4, 5], maxlen=6)
        deque.extendleft([2, 1, 0])

        deque.rotate(0)
        assert list(deque) == [0, 1, 2, 3, 4, 5]

        deque.rotate(1)
        assert list(deque) == [5, 0, 1, 2, 3, 4]

        deque.rotate(2)
        assert list(deque) == [3, 4, 5, 0, 1, 2]

        deque.rotate(6)
        assert list(deque) == [3, 4, 5, 0, 1, 2]

        deque.rotate(13)
        assert list(deque) == [2, 3, 4, 5, 0, 1]

        deque.rotate(-1)
        assert list(deque) == [3, 4, 5, 0, 1, 2]

        deque.rotate(-3)
        assert list(deque) == [0, 1, 2, 3, 4, 5]

        deque.rotate(-6)
        assert list(deque) == [0, 1, 2, 3, 4, 5]

        deque.rotate(-13)
        assert list(deque) == [1, 2, 3, 4, 5, 0]

    def test_maxlen_0(self):
        deque = RingDeque([1, 2, 3], maxlen=0)
        assert list(deque) == []

        deque.append(1)
        assert list(deque) == []

        deque.appendleft(1)
        assert list(deque) == []

        deque.extend([1, 2, 3])
        assert list(deque) == []

        deque.extendleft([1, 2, 3])
        assert list(deque) == []

        deque.rotate(10)
        assert list(deque) == []

    def test_repr(self):
        deque = RingDeque([1, 2, 3], maxlen=3)
        assert repr(deque) == 'RingDeque([1, 2, 3], maxlen=3)'

        deque = RingDeque(maxlen=3)
        assert repr(deque) == 'RingDeque([], maxlen=3)'

    def test_copy(self):
        for copy_func in [copy, lambda x: x.copy()]:
            original_deque = RingDeque([1, 2, 3], maxlen=5)
            copy_deque = copy_func(original_deque)
            assert original_deque is not copy_deque
            assert original_deque == copy_deque
            assert original_deque.maxlen == copy_deque.maxlen
            assert list(original_deque) == list(copy_deque)

            copy_deque.append(5)
            assert 5 in copy_deque
            assert 5 not in original_deque
            assert len(copy_deque) != len(original_deque)
            assert copy_deque != original_deque
            assert list(copy_deque) != list(original_deque)

    def test_eq(self):
        assert RingDeque([1, 2, 3], maxlen=4) == RingDeque([1, 2, 3], maxlen=4)
        assert RingDeque([1, 2, 3], maxlen=4) == RingDeque([1, 2, 3], maxlen=3)
        assert RingDeque([1, 2, 3], maxlen=4) != RingDeque([1, 3, 2], maxlen=4)
        assert RingDeque([1, 2, 3], maxlen=4) != [1, 2, 3]

    def test_clear(self):
        deque = RingDeque([3, 4, 5, 6], maxlen=10)
        deque.extendleft([2, 1, 0])
        deque.extend([7, 8, 9])
        assert list(deque) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        deque.clear()
        assert list(deque) == []

    def test_bool(self):
        assert not RingDeque(maxlen=3)
        assert not RingDeque([], maxlen=3)
        assert RingDeque([1, 2], maxlen=3)
        assert RingDeque([1, 2, 3], maxlen=3)

    def test_concatenation(self):
        deque = RingDeque([1, 2], maxlen=5) + RingDeque([3, 4], maxlen=7)
        assert list(deque) == [1, 2, 3, 4]
        assert deque.maxlen == 5

        deque = RingDeque([1, 2], maxlen=7) + RingDeque([3, 4], maxlen=5)
        assert list(deque) == [1, 2, 3, 4]
        assert deque.maxlen == 7

        with pytest.raises(TypeError):
            RingDeque([1, 2], maxlen=5) + [3, 4]  # noqa

        deque = RingDeque([1, 2], maxlen=5)
        deque += RingDeque([3, 4], maxlen=7)
        assert list(deque) == [1, 2, 3, 4]
        assert deque.maxlen == 5

        deque = RingDeque([1, 2], maxlen=5)
        deque += [3, 4]
        assert list(deque) == [1, 2, 3, 4]
        assert deque.maxlen == 5

    @pytest.mark.parametrize('items, maxlen, n, expected', [
        ([], 6, 2, []),
        ([1, 2, 3], 6, 2, [1, 2, 3, 1, 2, 3]),
        ([1, 2, 3], 5, 2, [2, 3, 1, 2, 3]),
        ([1, 2, 3], 6, 1, [1, 2, 3]),
        ([1, 2, 3], 6, 0, []),
        ([1, 2, 3], 6, -10, []),
    ])
    def test_multiplication(self, items, maxlen, n, expected):
        deque = RingDeque(items, maxlen=maxlen) * n
        assert deque.maxlen == maxlen
        assert list(deque) == expected

        deque = n * RingDeque(items, maxlen=maxlen)
        assert deque.maxlen == maxlen
        assert list(deque) == expected

        deque = RingDeque(items, maxlen=maxlen)
        assert deque.maxlen == maxlen
        deque *= n
        assert list(deque) == expected
