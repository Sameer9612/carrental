# Generated by Django 5.1.1 on 2025-01-16 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0008_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='address',
            field=models.TextField(default='company'),
        ),
        migrations.AddField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=10),
        ),
    ]
