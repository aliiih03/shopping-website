# Generated by Django 4.2.16 on 2025-04-27 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_shippingaddress_shipping_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
