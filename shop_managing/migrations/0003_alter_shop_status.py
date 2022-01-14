# Generated by Django 3.2.9 on 2022-01-14 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_managing', '0002_alter_shop_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='status',
            field=models.CharField(choices=[('Deleted', 'Deleted'), ('Confirmed', 'Confirmed'), ('Pending', 'Pending')], default='Pending', max_length=12),
        ),
    ]
