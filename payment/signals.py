from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ShippingAddress

@receiver(post_save,sender = User)
def create_shipping_address(sender,instance,created,**kwargs):
    if created:
        ShippingAddress.objects.create(user=instance)
