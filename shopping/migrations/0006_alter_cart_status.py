# Generated by Django 3.2.9 on 2022-01-05 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0005_alter_cart_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('deleted', 'Deleted'), ('paid', 'Paid'), ('confirmed', 'Confirmed')], default='pending', max_length=12),
        ),
    ]