from django.db import models

# Create your models here.
STATUS = (
    ('n', 'Новое'),
    ('a', 'Заказано'),
    ('d', 'Выполнено'),
    ('c', 'Отклонено'),
)

class Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    def __str__(self):
        return self.customer_name

class IkeaItem(models.Model):
    title = models.CharField(max_length=300)
    product_name = models.CharField(max_length=200)
    category_name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    code = models.IntegerField(default=0)
    url = models.URLField()
    picture_url = models.URLField()
    datetime = models.DateTimeField('date added')
    status = models.CharField(max_length=1, choices=STATUS)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return ('%s, %s руб.' % (self.title, self.price))
