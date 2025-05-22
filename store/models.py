from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create Customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.user.username

# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    description = models.TextField()
    image = models.ImageField(upload_to='product/uploads', blank=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product}'
