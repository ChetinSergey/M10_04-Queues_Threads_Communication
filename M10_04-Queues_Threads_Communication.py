import time
import threading
import queue


class Table:

    def __init__(self, number):
        self.number = number
        self.is_busy = False


class Cafe:

    def __init__(self, queue, tables):
        self.queue = queue
        self.tables = tables

    def customer_arrival(self):
        total_customer = 20
        for num_cust in range(1, total_customer + 1):
            print(f'Посетитель номер {num_cust} прибыл.')
            self.serve_customer(num_cust)
            time.sleep(2)

    def serve_customer(self, num_cust):
        check_table = False
        for table in tables:
            if not table.is_busy:
                somebody = Customer(num_cust, self, table)
                table.is_busy = True
                somebody.start()
                check_table = True
                break
        if not check_table:
            self.queue.put(num_cust)
            print(f'Посетитель {num_cust} ожидает свободный стол!')


class Customer(threading.Thread):
    def __init__(self, visitor, cafe, table, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visitor = visitor
        self.cafe = cafe
        self.table = table

    def run(self):
        self.table.is_busy = True
        print(f'Посетитель номер {self.visitor} сел за стол {self.table.number}. (начало обслуживания)')
        time.sleep(5)
        print(f'Посетитель номер {self.visitor} покушал и ушёл. (конец обслуживания)')
        self.table.is_busy = False
        if self.cafe.queue.qsize() > 0:
            self.cafe.serve_customer(self.cafe.queue.get())


# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
queue = queue.Queue()
queue.qsize()
cafe = Cafe(queue, tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()
