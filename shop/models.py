from django.db.models import Model, CharField, TextField, DecimalField, ImageField, DateTimeField, BooleanField, ForeignKey, CASCADE, ManyToManyField, PositiveIntegerField

# Create your models here.

class Category(Model):
    name = CharField(max_length=255, verbose_name='Название')
    description = TextField(verbose_name='Описание')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
class Tag(Model):
    name = CharField(max_length=255, verbose_name='Название')
    description = TextField(verbose_name='Описание')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Product(Model):
    name = CharField(max_length=255, verbose_name='Название')
    description = TextField(verbose_name='Описание')
    price = DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = ImageField(null=True, verbose_name='Изображение')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = DateTimeField(auto_now=True, verbose_name='Последнее изменение')
    is_deleted = BooleanField(default=False, verbose_name='Удалено')

    category = ForeignKey(Category, on_delete=CASCADE, related_name='products', verbose_name='Категория')
    tags = ManyToManyField(Tag, related_name='products', verbose_name='Теги')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
class Order(Model):
    number = CharField(max_length=20, unique=True, verbose_name='Номер')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Создано')
    delivery_address = CharField(max_length=255, verbose_name='Адрес доставки')
    phone = CharField(max_length=20, verbose_name='Телефон')
    customer_name = CharField(max_length=255, verbose_name='ФИО клиента')

    products = ManyToManyField(Product, through='OrderItem', verbose_name='Товары')
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderItem(Model):
    order = ForeignKey(Order, on_delete=CASCADE, verbose_name='Заказ')
    product = ForeignKey(Product, on_delete=CASCADE, verbose_name='Товар')
    quantity = PositiveIntegerField(verbose_name='Количество')
    discount = DecimalField(max_digits=5, decimal_places=2, verbose_name='Скидка')
    
    class Meta:
        verbose_name = 'Состав заказа'
        verbose_name_plural = 'Состав заказов'