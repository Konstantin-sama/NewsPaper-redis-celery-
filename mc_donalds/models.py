from django.db import models
from datetime import datetime
from mc_donalds.resources import POSITIONS, cashier
# from .resources import POSITIONS, cashier


class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, choices=POSITIONS, default=cashier)
    labor_contract = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    # take_away
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='orders')

    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds()
            # //60  в минутах
        else:
            return (datetime.now() - self.time_in).total_secouds()
            # //60
        # USE_TZ = False from settings.py


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    def product_sum(self):
        return self.product.price * self._amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()


# Create your models here.

# CREATE TABLE STAFF (
#     staff_id INT AUTO_INCREMENT NOT NULL,
#     full_name CHAR(255) NOT NULL,
#     position CHAR(255) NOT NULL,
#     labor_contract INT NOT NULL,
#
#     PRIMARY KEY (staff_id)
# );

# CREATE TABLE PRODUCTS (
#     product_id INT AUTO_INCREMENT NOT NULL,
#     name CHAR(255) NOT NULL,
#     price FLOAT NOT NULL,
#
#     PRIMARY KEY (product_id)
# );

# CREATE TABLE ORDERS(
#   order_id INT AUTO_INCREMENT NOT NULL,
#   time_in DATETIME NOT NULL,
#   time_out DATETIME,
#   cost FLOAT NOT NULL,
#   take_away INT NOT NULL,
#
#   staff INT NOT NULL,
#
#   PRIMARY KEY(order_id),
#   FOREIGN KEY(staff) REFERENCES STAFF(staff_id)
# );

# director = 'DI'
# admin = 'AD'
# cook = 'CO'
# cashier = 'CA'
# cleaner = 'CL'
# POSITIONS = [
#     (director, 'Директор'),
#     (admin, 'Администратор'),
#     (cook, 'Повар'),
#     (cashier, 'Кассир'),
#     (cleaner, 'Уборщик')
# ]

    # заполнение базы данных через shell
# python manage.py shell
# from mc_donalds.models import *

# cap = Product(name = "Капучино 0.3", price = 99.0)
# cap.save()

# Product.obje
# результат: Product.obje

# Product.objects.create(name="Капучино 0.4", price=109.0)
# результат: < Product: Product.object (2)>

# cashier1 = Staff.objects.create(full_name = "Иванов Иван Иванович",
#                                 position = Staff.cashier,
#                                 labor_contract = 1754)
# cashier2 = Staff.objects.create(full_name = "Петров Петр Петрович",
#                                 position = Staff.cashier,
#                                 labor_contract = 4355)
# direct = Staff.objects.create(full_name = "Максимов Максим Максимович",
#                                 position = Staff.director,
#                                 labor_contract = 1254)

    # Поиск информации через shell      # 1 урок(вебинар)

    # уникальный объект - get
# Staff.objects.get(pk=1)
# результат: <Staff: Staff object (1)>

# Staff.objects.get(pk=1).full_name
# результат: "Иванов Иван Иванович"

# Staff.objects.get(labor_contract = 4355).full_name
# результат: "Петров Петр Петрович"

# Staff.objects.get(position='CA').full_name
# результат: ERROR потому что не уникальный фильтр (объекта 2)

# Staff.objects.get(position='DI').full_name
# результат:"Максимов Максим Максимович"

# результат получен с учетом уникальности (объект 1)

    # чтобы вывести несколько объектов - filter
# Staff.objects.filter(position='CA')
# результат: <QuerySet [<Staff: Staff object (1)>,<Staff: Staff object (2)>]>

# Product.objects.filter(price__gt = 100.0)
# результат: <QuerySet [<Product: Product object (2)>]>

    # чтобы вывести все объекты - all()
# Product.objects.all()
# результат: <QuerySet [<Product: Product object (1)>, <Product: Product object (2)>]>

    # Создание объектов моделей     # Модуль (теория)
# cap = Product(name = "Монитор", price = 9999.0)
# cap.save()
# или
# cap_big = Product.objects.create(name = "Монитор", price = 9999.0)


# product_1 = Product(name = "Витая пара (3 м)", price = 993.0)
# product_1.save()
#
# product_2 = Product.objects.create(name = "Клавиатура", price = 1060.0)

    # инструкция как добавлять товары в базу данных
# python manage.py shell
# from mc_donalds.models import Product

# product_1 = Product(name = "Витая пара 3 м", price = 309.0)
# product_1.save()
# product_2 = Product.objects.create(name = "Витая пара 1 м", price = 109.0)

    # Получение объектов модели, метод get

# cashier1 = Staff.objects.create(full_name = "Иванов Иван Иванович",
#                                 position = Staff.cashier,
#                                 labor_contract = 1754)
# cashier2 = Staff.objects.create(full_name = "Петров Петр Петрович",
#                                 position = Staff.cashier,
#                                 labor_contract = 4355)
# direct = Staff.objects.create(full_name = "Максимов Максим Максимович",
#                                 position = Staff.director,
#                                 labor_contract = 1254)

# поиск по контракту
# person = Staff.objects.get(labor_contract = 1254)
# результат: ??? скорее всего index

# person = Staff.objects.get_position_display(pk=3)
# результат: директор

# person = Staff.objects.get(pk=3).full_name
# результат: "Максимов Максим Максимович"

# person = Staff.objects.get(pk=3).position
# результат: DI

# получаем всех кассиров
# cashiers = Staff.objects.get(position = Staff.cashier)
# результат: Мы получим ошибку от Django

# нужно применить метод filter()
# cashiers = Staff.objects.filter(position = Staff.cashier)
# результат: список индексов всех объектов (кассиров)

    # добавление в базу данных новостной портал (газета)
# a = Author(full_name = "Иванов Иван Иванович")
# a.save()
# или
# Author.objects.create(full_name = "Иванов Иван Иванович")
# также можно
# Author.objects.create(full_name="Иванов Иван Иванович" age=25, email="i_ivan@example.com")

# Как получить автора с именем «Петров Петр Петрович»?
# Author.objects.create(full_name='Иванов Иван Иванович')
# Author.objects.create(full_name='Петров Петр Петрович')
# Author.objects.create(full_name='Максимов Максим Максимович')
# ответ:
# Author.objects.get(pk=3)

    # Метод filter()
# Staff.objects.filter(position = Staff.cashier)
# результат: <QuerySet [<Staff: Staff object (1)>, <Staff: Staff object (2)>]>

# cashiers = Staff.objects.filter(position = Staff.cashier)
# результат: <QuerySet [<Staff: Staff object (1)>, <Staff: Staff object (2)>]>
# cashiers.values("full_name", "labor_contract")
# Вернёт два объекта: <QuerySet [{'full_name'='Иванов Иван Иванович': 'labor_contract'=1754},
#                               {'full_name'='Петров Петр Петрович': 'labor_contract'=4355}]>

# Product.objects.filter(price__gt = 90.0).values("name")
# Вернёт два объекта: <QuerySet [{'name': 'Витая пара 3 м'}, {'name': 'Витая пара 1 м'}]>

# Отдельно остановимся на методе фильтрации по связанным объектам.
# Добавим несколько объектов в модель Order.

# from mc_donalds.models import Order
# Order.objects.create(staff = cashier1, pickup = False)
# Order.objects.create(staff = cashier2, pickup = True)
# Order.objects.create(staff = cashier1, pickup = True)

# мы хотим получить все заказы сотрудника с labor_contract = 1754.
# Order.objects.filter(staff__labor_contract = 1754).values("staff__full_name", "pickup")

# В результате имеем два объекта:
# <QuerySet [{'staff__full_name': 'Иванов Иван Иванович', 'pickup': False},
# {'staff__full_name': 'Иванов Иван Иванович', 'pickup': True}]>

    #  метод менеджера all()
# Product.objects.all().values("name")
# В результате имеем все:
# <QuerySet [{'name': 'Витая пара 3 м'}, {'name': 'Витая пара 1 м'},
#           {'name': 'Монитор'}, {'name': 'Клавиатура'}]>

    # ProductOrder сейчас ещё нет абсолютно ничего
# >>> from rest.Models import ProductOrder
# >>> ProductOrder.objects.all()
# <QuerySet []>

# QuerySet есть также свои методы,
# и один из них проверяет наличие каких-либо объектов в результате запроса.
# >>> ProductOrder.objects.all().exists()
# False

    # метод сортировки order_by(‘field_name’)
# получить отсортированный по ценам список товаров
# >>> Product.objects.all().order_by('price').values('name', 'price')
# В такой записи объекты сортируются в порядке возрастания

# отсортировать в порядке убывания
# перед названием поля внутри этого метода поставить знак «-» (минус)
# >>> Product.objects.all().order_by('-price').values('name', 'price')

# отфильтровать модель Author на те сущности, age которых меньше 25
# Author.objects.filter(age__lt = 25)

    # Вебинар про время заказа
# from mc_donalds.models import *

# Staff.objects.all()
# результат: <QuerySet [<Staff: Staff object (1)>, <Staff: Staff object (2)>, <Staff: Staff object (3)>]>

# Staff.objects.all().first()
# результат: <Staff: Staff object (1)>

# order = Order.objects.create(staff=ca)
# order
# результат: <Order: Order object (4)>

# order.get_duration()
# результат: 28.441559
# order.get_duration()
# результат: 31.571643

# order.finish_order()
# order.get_duration()
# результат: 35.571643
# order.get_duration()
# результат: 35.571643

# p1 = Product.objects.all()[0]
# p2 = Product.objects.all()[1]

# p1
# результат: <Product: Product object (1)>
# p2
# результат: <Product: Product object (2)>

# order
# результат: <Order: Order object (4)>

# order.products.add(p1)
# order.products.add(p2)

# order.products.all()
# результат: <QuerySet [<Product: Product object (1)>, <Product: Product object (2)>]

# order.products.all().values('name')
# результат: <QuerySet [{'name': 'Капучино 0.3'}, {'name': 'Капучино 0.4'}]>

# order.products.all().values('name','price')
# результат: <QuerySet [{'name': 'Капучино 0.3', 'price': 99.0},
#                       {'name': 'Капучино 0.4', 'price': 109.0}]>

    # ca = check all(order) / 1cashier = ca
# ca
# результат: <Staff: Staff object (1)>

# ca.order_set.all()
# результат: <QuerySet [<Order: Order object (4)>]>

# Order.objects.create(staff=ca)
# результат: <Order: Order object (5)>

# ca.order_set.all()
# результат: <QuerySet [<Order: Order object (4)>, <Order: Order object (5)>]>

    # staff = models.ForeignKey(related_name='orders')
# from mc_donalds.models import *
# ca = Staff.objects.all().first()
# ca.orders.all()
# результат: <QuerySet [<Order: Order object (4)>, <Order: Order object (5)>]>

    # запрос к таблице Author, поле age у которых равен 32 (число), взяв только поле name
# Author.objects.filter(age=32).values("name")
# результат: <QuerySet [{“name”: “Иванов Иван”}, … ] >