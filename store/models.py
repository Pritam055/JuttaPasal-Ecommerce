from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    STOCK = (
        ("In Stock", "In Stock"),
        ("Out of Stock", "Out of Stock")
    )
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=300, default="", null=True, blank=True)
    image = models.ImageField(upload_to="uploads/products/")
    stock = models.CharField(max_length=20, choices=STOCK)
    qty = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def get_product_by_ids(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_product_by_id(id):
        return Product.objects.get(id=id)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to='uploads/customer/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    @staticmethod
    def get_customer_by_id(id):
        return Customer.objects.get(id=id)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default="", blank=True)
    phone = models.CharField(max_length=10, default="", blank=True)
    # date = models.DateField(default=datetime.datetime.today)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()
