# Generated by Django 4.2.16 on 2025-04-19 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_profile_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='old_cart',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
