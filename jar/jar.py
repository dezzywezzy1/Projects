
class Jar:
    def __init__(self, capacity=12):
        if capacity not in range(13):
            raise ValueError("Not enough capacity")
        self._capacity = capacity
        self.size = 0


    def __str__(self):
        return "🍪" * self.size

    def deposit(self, n):
        self.size += n
        if self.size > 12:
            raise ValueError("Not enough capacity")

    def withdraw(self, n):
        self.size -= n
        if self.size < 0:
            raise ValueError("Not enough cookies in jar")

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self,n):
        self._capacity = n


    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, n):
        self._size = n



def main():
    jar = Jar()
    print(str(jar.capacity))
    print(str(jar))
    jar.deposit(2)
    print(str(jar))
    jar.withdraw(11)
    print(str(jar))


main()