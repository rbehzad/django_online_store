# Generated by Django 3.2.9 on 2022-01-12 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0015_alter_cart_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Pending', 'Pending'), ('Canceled', 'Canceled'), ('Paid', 'Paid')], default='pending', max_length=12),
        ),
    ]
